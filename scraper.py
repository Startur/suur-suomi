import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from database import SessionLocal
from models import Article
import time
from datetime import datetime
import os

# HS.fi RSS Feeds
HS_RSS_FEEDS = [
    {"name": "Helsingin Sanomat", "url": "http://www.hs.fi/rss/suomi.xml"},
    {"name": "Helsingin Sanomat", "url": "http://www.hs.fi/rss/maailma.xml"},
    {"name": "Helsingin Sanomat", "url": "https://www.hs.fi/rss/politiikka.xml"}
]

def article_exists(link):
    """Checks if an article with the given link already exists in the database."""
    db = SessionLocal()
    exists = db.query(Article).filter_by(source_url=link).first() is not None
    db.close()
    return exists

def scrape_hs_rss():
    """Fetches article links from HS.fi RSS feeds and extracts full article content with metadata."""
    articles = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for feed in HS_RSS_FEEDS:
        response = requests.get(feed["url"], headers=headers)
        if response.status_code != 200:
            print(f"⚠️ Failed to fetch RSS feed: {feed['url']}")
            continue

        root = ET.fromstring(response.content)
        article_count = 0  # Track the number of articles scraped

        for item in root.findall(".//item"):
            if article_count >= 10:  # Stop after scraping 10 articles (for testing)
                break

            title = item.find("title").text
            link = item.find("link").text

            if article_exists(link):
                print(f"⏩ Skipping duplicate article: {title}")
                continue

            published_at = item.find("pubDate").text if item.find("pubDate") else None
            author = item.find("dc:creator").text if item.find("dc:creator") else "Tuntematon"
            source = feed["name"]

            if published_at:
                try:
                    published_at = datetime.strptime(published_at, "%a, %d %b %Y %H:%M:%S %z")
                except ValueError:
                    published_at = None

            full_content, published_at = fetch_full_article(link)

            if full_content:
                save_article(title, link, full_content, published_at, source)
                articles.append({"title": title, "url": link, "content": full_content, "source": source, "author": author, "published_at": published_at})
                article_count += 1

            time.sleep(1)

    return articles

def fetch_full_article(url):
    """Fetches and extracts full article content and publication date from a given URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch article: {url}")
            return None, None

        soup = BeautifulSoup(response.text, "html.parser")
        date_element = soup.select_one("meta[itemprop='datePublished']")
        published_at = date_element["content"] if date_element else None
        print(f"📅 Extracted published_at: {published_at} for {url}")

        article_body = soup.select_one("div.article-body")
        if not article_body:
            article_body = soup.find("div", class_="hs-article-content")
        if not article_body:
            article_body = soup.find("article")

        if article_body:
            paragraphs = article_body.find_all("p")
            content = "\n".join([p.get_text(strip=True) for p in paragraphs]) if paragraphs else article_body.get_text(strip=True)
            return content, published_at
        else:
            print(f"Could not find article content for: {url}")
            return None, None

    except Exception as e:
        print(f"Error extracting article content from {url}: {e}")
        return None, None

def save_article(title, url, content, published_at, source):
    """Stores the article in the database if it's not already saved."""
    db = SessionLocal()
    existing_article = db.query(Article).filter_by(source_url=url).first()
    if not existing_article:
        print(f"✅ Saving article: {title}, Published At: {published_at}")
        new_article = Article(
            title=title,
            content=content,
            source_url=url,
            source=source,
            published_at=published_at if published_at else None
        )
        db.add(new_article)
        db.commit()
    db.close()

if __name__ == "__main__":
    articles = scrape_hs_rss()
    print(f"✅ Scraped {len(articles)} full articles from HS.fi RSS")
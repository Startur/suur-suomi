import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from database import SessionLocal
from models import Article

# HS.fi RSS Feeds
HS_RSS_FEEDS = [
    "http://www.hs.fi/rss/suomi.xml",  # Domestic
    "http://www.hs.fi/rss/maailma.xml",  # World news
    "https://www.hs.fi/rss/politiikka.xml", # Politics
    "http://www.hs.fi/rss/talous.xml",  # Economy
]

def scrape_hs_rss():
    """Fetches article links from HS.fi RSS feeds and extracts full article content."""
    articles = []

    for feed_url in HS_RSS_FEEDS:
        response = requests.get(feed_url)
        if response.status_code != 200:
            print(f"Failed to fetch RSS feed: {feed_url}")
            continue

        root = ET.fromstring(response.content)

        for item in root.findall(".//item"):
            title = item.find("title").text
            link = item.find("link").text
            full_content = fetch_full_article(link)

            if full_content:
                save_article(title, link, full_content)
                articles.append({"title": title, "url": link, "content": full_content})

    return articles

def fetch_full_article(url):
    """ Fetches and extracts full article content from a given URL. """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch article: {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the main article content
    article_section = soup.find("section", class_="article-body")
    
    if article_section:
        paragraphs = article_section.find_all("p", class_="article-body")
        return "\n".join(p.get_text(strip=True) for p in paragraphs)
    else:
        print(f"Could not extract article content: {url}")
        return None

def save_article(title, url, content):
    """Stores the article in the database if it's not already saved."""
    db = SessionLocal()
    existing_article = db.query(Article).filter_by(source_url=url).first()
    if not existing_article:
        new_article = Article(title=title, content=content, source_url=url)
        db.add(new_article)
        db.commit()
    db.close()

if __name__ == "__main__":
    articles = scrape_hs_rss()
    print(f"Scraped {len(articles)} full articles from HS.fi RSS")

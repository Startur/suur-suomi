import psycopg2

# Database connection settings (update credentials)
DB_SETTINGS = {
    "dbname": "news_platform",
    "user": "news_admin",
    "password": "iuvbiu23223",  # Replace with your actual PostgreSQL password
    "host": "localhost"
}

def list_articles():
    """Fetch all newly scraped articles that are not yet selected for rewriting."""
    conn = psycopg2.connect(**DB_SETTINGS)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title FROM articles WHERE selected_for_rewrite = FALSE ORDER BY created_at DESC;")
    articles = cursor.fetchall()

    if not articles:
        print("✅ No new articles available for selection.")
    else:
        print("\n📌 **Available Articles for Rewriting:**")
        for article in articles:
            print(f"{article[0]}: {article[1]}")

    cursor.close()
    conn.close()

def select_articles():
    """Allows user to manually select which articles should be rewritten."""
    list_articles()
    article_ids = input("\nEnter the article IDs to be rewritten (comma-separated): ").strip()
    
    if not article_ids:
        print("⚠️ No articles selected.")
        return

    article_ids = [int(i) for i in article_ids.split(",")]

    conn = psycopg2.connect(**DB_SETTINGS)
    cursor = conn.cursor()

    query = "UPDATE articles SET selected_for_rewrite = TRUE WHERE id = ANY(%s)"
    cursor.execute(query, (article_ids,))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ Selected {len(article_ids)} articles for rewriting.")

if __name__ == "__main__":
    select_articles()
import psycopg2
from ai_rewriter import rewrite_article
import logging

# Database connection settings
DB_SETTINGS = {
    "dbname": "news_platform",
    "user": "news_admin",
    "password": "your_password",  # Replace with actual credentials
    "host": "localhost"
}

# Configure logging
logging.basicConfig(
    filename="batch_rewrite.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def process_batch():
    """Fetches all articles selected for rewriting and processes them."""
    conn = psycopg2.connect(**DB_SETTINGS)
    cursor = conn.cursor()

    # ✅ Fetch selected articles and print for debugging
    cursor.execute("SELECT id, content FROM articles WHERE selected_for_rewrite = TRUE AND id NOT IN (SELECT original_article_id FROM rewritten_articles)")
    articles = cursor.fetchall()

    if not articles:
        logging.error("❌ ERROR: Articles are marked for rewriting, but the script is not fetching them!")
        print("❌ ERROR: Articles are marked for rewriting, but the script is not fetching them!")
        print("🔹 Check if `rewritten_articles` table has unexpected data.")
        return  # ✅ Prevent further execution

    logging.info(f"🔹 Articles selected for rewriting: {[article[0] for article in articles]}")
    print(f"🔹 Articles selected for rewriting: {[article[0] for article in articles]}")

    for article_id, content in articles:
        rewritten_text = rewrite_article(article_id, content)

        if not rewritten_text or rewritten_text.strip() == "":
            logging.warning(f"⚠️ AI returned empty content for article {article_id}. Skipping...")
            print(f"⚠️ AI returned empty content for article {article_id}. Skipping...")
            continue  # ✅ Skip saving empty rewrites

        logging.info(f"✅ Saving rewritten article {article_id}: {rewritten_text[:100]}...")  # Print first 100 chars
        print(f"✅ Saving rewritten article {article_id}: {rewritten_text[:100]}...")

        cursor.execute(
            "INSERT INTO rewritten_articles (original_article_id, rewritten_content, editor_approved, created_at) VALUES (%s, %s, %s, NOW())",
            (article_id, rewritten_text, False)
        )
        conn.commit()

    cursor.close()
    conn.close()
    logging.info("✅ Batch processing completed successfully.")

if __name__ == "__main__":
    process_batch()
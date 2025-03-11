import psycopg2
import openai
import os
from datetime import datetime

# Load API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

# Database connection settings (securely using environment variables)
DB_SETTINGS = {
    "dbname": os.getenv("DB_NAME", "news_platform"),
    "user": os.getenv("DB_USER", "news_admin"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost")
}

def save_to_database(original_article_id, rewritten_text):
    """Saves the rewritten article to PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cursor = conn.cursor()

        query = """
        INSERT INTO rewritten_articles (original_article_id, rewritten_content, editor_approved, created_at)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (original_article_id, rewritten_text, False, datetime.now()))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Successfully saved article {original_article_id} to database.")
    except Exception as e:
        print(f"❌ Database error: {e}")

def update_article_status_to_rewritten(original_article_id):
    """Updates the rewrite_status of the article to 'rewritten' in the database."""
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cursor = conn.cursor()

        query = """
        UPDATE articles
        SET rewrite_status = %s
        WHERE id = %s
        """
        cursor.execute(query, ('rewritten', original_article_id))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Article {original_article_id} status updated to 'rewritten'.")
    except Exception as e:
        print(f"❌ Failed to update article status: {e}")

def select_articles(article_id):
    """Allows user to manually select which articles should be rewritten and updates their status."""
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cursor = conn.cursor()

        # Update the article status to 'selected_for_rewriting'
        query = """
        UPDATE articles
        SET rewrite_status = %s
        WHERE id = %s
        """
        cursor.execute(query, ('selected_for_rewriting', article_id))

        conn.commit()
        cursor.close()
        conn.close()

        print(f"✅ Article {article_id} selected for rewriting.")

    except Exception as e:
        print(f"❌ Failed to select article {article_id}: {e}")

def rewrite_article(original_article_id, article_text):
    """Rewrites the article using OpenAI's GPT-4 and saves it to the database."""

    if not OPENAI_API_KEY:
        return "⚠️ OpenAI API key is missing."

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""
    Kirjoita tämä uutinen täysin uudelleen kansallismielisestä ja taloudellisesti konservatiivisesta näkökulmasta.
    - Älä kopioi alkuperäistä uutista, vaan muokkaa se uusiksi täysin uudella rakenteella.
    - Korosta Suomen omavaraisuutta, taloudellista riippumattomuutta ja kansallista etua.
    - Vältä monikulttuurisuuden ja globalisaation ylikorostamista.
    - Käytä selkeää ja suoraa journalistista tyyliä.
    - Perustele väitteet loogisesti faktoihin pohjautuen.

    **Alkuperäinen uutinen:**
    {article_text}

    ✍️ **Uudelleenkirjoitettu uutinen:**
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Sinä olet kokenut suomalainen toimittaja, joka kirjoittaa kansallismielisestä ja taloudellisesti konservatiivisesta näkökulmasta. Uutiset on kirjoitettava selkeästi, loogisesti ja asiapohjaisesti."},
                      {"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.3
        )

        rewritten_text = response.choices[0].message.content.strip()
        print(f"🔹 AI Output for article {original_article_id}: {rewritten_text[:100]}...")  # Print first 100 chars
        
        save_to_database(original_article_id, rewritten_text)
        update_article_status_to_rewritten(original_article_id)
        
        return rewritten_text

    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return None

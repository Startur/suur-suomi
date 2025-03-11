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
        return rewritten_text

    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return None

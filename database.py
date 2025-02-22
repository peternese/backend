import os
import psycopg2

# PostgreSQL-Verbindungsdetails aus Umgebungsvariable
DATABASE_URL = os.environ.get("DATABASE_URL")

# Verbindung zur PostgreSQL-Datenbank herstellen
conn = psycopg2.connect(DATABASE_URL, sslmode="disable")
c = conn.cursor()

# Tabelle erstellen, falls sie nicht existiert
c.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        short TEXT PRIMARY KEY, 
        original TEXT
    )
""")
conn.commit()

# Funktion zum Speichern einer URL
def save_url(short: str, original: str):
    c.execute("INSERT INTO urls (short, original) VALUES (%s, %s)", (short, original))
    conn.commit()

# Funktion zum Abrufen einer originalen URL
def get_original_url(short: str):
    c.execute("SELECT original FROM urls WHERE short=%s", (short,))
    return c.fetchone()

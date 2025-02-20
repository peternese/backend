from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random, string
import sqlite3
import uvicorn
import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")

app = FastAPI()

BASE_URL = "https://quickgraeff.onrender.com"

# SQLite Datenbank Verbindung
conn = psycopg2.connect(DATABASE_URL, sslmode="require")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS urls (short TEXT PRIMARY KEY, original TEXT)")
conn.commit()

# Model für die API-Anfragen
class URLRequest(BaseModel):
    original_url: str

# Funktion zum Generieren einer Kurz-URL
def generate_short_url(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# API-Endpunkt: URL kürzen
@app.post("/shorten/")
def shorten_url(url_data: URLRequest):
    short = generate_short_url()
    c.execute("INSERT INTO urls (short, original) VALUES (%s, %s)", (short, url_data.original_url))
    conn.commit()
    return {"short_url": f"{BASE_URL}/{short}"}

# API-Endpunkt: URL auflösen
@app.get("/{short_url}")
def redirect(short_url: str):
    c.execute("SELECT original FROM urls WHERE short=%s", (short_url,))
    result = c.fetchone()
    if result:
        return {"redirect_to": result[0]}
    raise HTTPException(status_code=404, detail="URL not found")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render setzt automatisch einen Port
    uvicorn.run(app, host="0.0.0.0", port=port)

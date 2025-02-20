from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random, string
import sqlite3

app = FastAPI()

# SQLite Datenbank Verbindung
conn = sqlite3.connect("urls.db", check_same_thread=False)
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
    c.execute("INSERT INTO urls (short, original) VALUES (?, ?)", (short, url_data.original_url))
    conn.commit()
    return {"short_url": f"https://your-backend-url.com/{short}"}

# API-Endpunkt: URL auflösen
@app.get("/{short_url}")
def redirect(short_url: str):
    c.execute("SELECT original FROM urls WHERE short=?", (short_url,))
    result = c.fetchone()
    if result:
        return {"redirect_to": result[0]}
    raise HTTPException(status_code=404, detail="URL not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

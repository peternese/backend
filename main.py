from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import random, string
from models import URLRequest
from database import save_url, get_original_url
import uvicorn
import os

app = FastAPI()

BASE_URL = "https://quickgraeff.onrender.com"

@app.get("/")
def root():
    return {"message": "URL Shortener API is running! Use /shorten/ to shorten URLs. Powered by Peter Graeff."}

# Funktion zum Generieren einer Kurz-URL
def generate_short_url(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# API-Endpunkt: URL kürzen
@app.post("/shorten/")
def shorten_url(url_data: URLRequest):
    short = generate_short_url()
    save_url(short, url_data.original_url) # Datenbankeintrag über database.py speichern
    return {"short_url": f"{BASE_URL}/{short}"}

# API-Endpunkt: URL auflösen
@app.get("/{short_url}")
def redirect(short_url: str):
    result = get_original_url(short_url) # Datenbanabfrage über database.py
    if result:
        return RedirectResponse(url=result[0], status_code=307)  # 307 behält Methode (z. B. POST)
    raise HTTPException(status_code=404, detail="URL not found")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render setzt automatisch einen Port
    uvicorn.run(app, host="0.0.0.0", port=port)

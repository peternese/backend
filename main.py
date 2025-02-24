from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import random, string
from models import URLRequest
from database import save_url, get_original_url, get_short_url
import uvicorn
import requests
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://quickgraeff.vercel.app",  # Dein Frontend auf Vercel
    "http://localhost:3000",  # Falls du lokal testest
]

# ✅ CORS Middleware hinzufügen
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Hier kannst du deine Frontend-URL einfügen, z. B. ["https://quickgraeff.vercel.app"]
    allow_credentials=True,
    allow_methods=["GET","POST","OPTIONS"],  # Erlaubt alle Methoden (GET, POST, OPTIONS usw.)
    allow_headers=["*"],  # Erlaubt alle Header
    expose_headers=["Location"]  # ✅ WICHTIG für Redirects!
)

BASE_URL = "https://quickgraeff.vercel.app"

@app.get("/")
def root():
    return {"message": "URL Shortener API is running! Use /shorten/ to shorten URLs. Powered by Peter Graeff."}

# Funktion zur Überprüfung der URL-Erreichbarkeit
def check_url_exists(url: str) -> bool:
    try:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url  # Standardmäßig HTTPS verwenden

        print(f"🔍 Checking URL: {url}")  # Debugging

        response = requests.get(url, allow_redirects=True, timeout=5)

        print(f"✅ URL Status Code: {response.status_code}")  # Debugging

        return response.status_code < 400 or response.status_code == 403  # 403 zulassen
    except requests.RequestException as e:
        print(f"❌ Error checking URL {url}: {e}")  # Debugging
        return False


# Funktion zum Generieren einer Kurz-URL
def generate_short_url(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# API-Endpunkt: URL kürzen
@app.post("/shorten/")
def shorten_url(url_data: URLRequest):
    # Prüfen, ob die URL existiert
    if not check_url_exists(url_data.original_url):
        raise HTTPException(status_code=400, detail="The provided URL does not exist or is unreachable. Please try again.")

    # 🔍 Prüfen, ob die URL bereits existiert
    existing_short = get_short_url(url_data.original_url)
    if existing_short:
        return {"short_url": f"{BASE_URL}/{existing_short}"}  # Falls ja, gib die existierende zurück

    # Falls nicht, erstelle eine neue
    short = generate_short_url()
    save_url(short, url_data.original_url)  # Speichern in der Datenbank
    return {"short_url": f"{BASE_URL}/{short}"}

# API-Endpunkt: URL auflösen
@app.get("/{short_url}")
def redirect(short_url: str):
    result = get_original_url(short_url)  # Datenbankabfrage
    
    if result:
        print(f"🚀 Redirecting user to: {result}")  # Debugging
        return RedirectResponse(url=result, status_code=308)  # ✅ 308 erzwingt Browser-Redirect

    raise HTTPException(status_code=404, detail="URL not found")

@app.options("/{full_path:path}")
async def preflight_handler():
    return {"message": "CORS preflight successful"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render setzt automatisch einen Port
    uvicorn.run(app, host="0.0.0.0", port=port)

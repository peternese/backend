import os
import requests
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Set Supabase API details
# SUPABASE_URL = os.environ.get("SUPABASE_URL")
# SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

### ✅ Corrected Save URL function
def save_url(short: str, original: str):
    data = {"short": short, "original": original}
    
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/urls",
        json=[data],  # ✅ Supabase requires an array for inserting
        headers=HEADERS
    )
    # print(response.status_code)
    # print("📝 Insert Response:", response.status_code, response.text)
    # return response.json()

def get_short_url(original: str):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/urls?original=eq.{original}",
        headers=HEADERS
    )

    print("🔍 Checking if URL exists in DB:", response.status_code, response.text)

    if response.status_code != 200:
        return None  

    data = response.json()

    if not data:
        return None  # URL existiert nicht

    return data[0].get("short")  # Bestehenden Shortcode zurückgeben


def get_original_url(short: str):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/urls?short=eq.{short}",
        headers=HEADERS
    )

    print("🔍 Supabase Response:", response.status_code, response.text)

    if response.status_code != 200:
        return None  
    
    data = response.json()
    
    print("📦 Data Received:", data)  # Debugging

    if not data:  
        return None

    original_url = data[0].get("original")
    print(f"🔗 Redirecting to: {original_url}")  # Neue Debugging-Zeile
    return original_url  # Safely return original URL
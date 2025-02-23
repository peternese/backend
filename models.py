from pydantic import BaseModel, field_validator
import re

class URLRequest(BaseModel):
    original_url: str

    @field_validator("original_url")
    @classmethod
    def validate_and_format_url(cls, value):
        # 🔍 Falls die URL mit http:// oder https:// beginnt, entferne sie
        value = re.sub(r"^https?://", "", value)  # Entfernt "http://" oder "https://"

        # ✅ Falls kein Schema existiert, füge "http://" hinzu
        formatted_url = "http://" + value  # Standardmäßig HTTP hinzufügen

        print(f"🔄 Formatted URL: {formatted_url}")  # Debugging
        return formatted_url

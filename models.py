from pydantic import BaseModel, field_validator

class URLRequest(BaseModel):
    original_url: str

    @field_validator("original_url")
    @classmethod
    def validate_and_format_url(cls, value):
        # Falls die URL kein Schema hat, füge 'http://' hinzu
        if not value.startswith(("http://", "https://")):
            value = "http://" + value
        return value

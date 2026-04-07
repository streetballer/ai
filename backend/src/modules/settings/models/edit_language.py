import re
from pydantic import BaseModel, field_validator


class EditLanguageBody(BaseModel):
    language: str

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        if not re.match(r"^[a-z]{2}$", value):
            raise ValueError("Language must be a valid ISO 639 two-letter code")
        return value

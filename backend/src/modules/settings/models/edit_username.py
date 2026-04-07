import re
from pydantic import BaseModel, field_validator


class EditUsernameBody(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]{3,20}$", value):
            raise ValueError("Username must be 3–20 characters: letters, numbers, and underscores only")
        return value

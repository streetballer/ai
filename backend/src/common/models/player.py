from dataclasses import dataclass
from datetime import datetime
from typing import Any, ClassVar


@dataclass
class Player:
    PUBLIC_PROJECTION: ClassVar[dict] = {"_id": 1, "username": 1, "language": 1, "team_id": 1}

    id: str
    email: str = ""
    email_verified: bool = False
    username: str = ""
    password_hash: str = ""
    refresh_token_hash: str = ""
    google_id: str = ""
    apple_id: str = ""
    facebook_id: str = ""
    language: str = "en"
    rating: int = 5
    geolocation: dict | None = None
    geolocation_timestamp: datetime | None = None
    team_id: str = ""
    created: datetime | None = None

    @classmethod
    def from_doc(cls, doc: dict[str, Any]) -> "Player":
        return cls(
            id=str(doc["_id"]),
            email=doc.get("email", ""),
            email_verified=doc.get("email_verified", False),
            username=doc.get("username", ""),
            password_hash=doc.get("password_hash", ""),
            refresh_token_hash=doc.get("refresh_token_hash", ""),
            google_id=doc.get("google_id", ""),
            apple_id=doc.get("apple_id", ""),
            facebook_id=doc.get("facebook_id", ""),
            language=doc.get("language", "en"),
            rating=doc.get("rating", 5),
            geolocation=doc.get("geolocation"),
            geolocation_timestamp=doc.get("geolocation_timestamp"),
            team_id=doc.get("team_id", ""),
            created=doc.get("created"),
        )

    def to_doc(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "email": self.email,
            "email_verified": self.email_verified,
            "username": self.username,
            "password_hash": self.password_hash,
            "refresh_token_hash": self.refresh_token_hash,
            "google_id": self.google_id,
            "apple_id": self.apple_id,
            "facebook_id": self.facebook_id,
            "language": self.language,
            "rating": self.rating,
            "geolocation": self.geolocation,
            "geolocation_timestamp": self.geolocation_timestamp,
            "team_id": self.team_id,
            "created": self.created,
        }

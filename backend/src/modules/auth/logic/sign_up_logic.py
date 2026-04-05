from datetime import datetime, timezone
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from src.common.libraries.database import get_database
from src.common.libraries.hash import hash_value
from src.common.libraries.jwt import create_access_token, create_refresh_token


def create_player(username: str, email: str, password: str) -> tuple[str | None, dict | None]:
    player_id = str(ObjectId())
    access_token = create_access_token(player_id)
    refresh_token = create_refresh_token(player_id)
    player_doc = {
        "_id": player_id,
        "email": email,
        "email_verified": False,
        "username": username,
        "password_hash": hash_value(password),
        "refresh_token_hash": hash_value(refresh_token),
        "google_id": "",
        "apple_id": "",
        "facebook_id": "",
        "language": "en",
        "rating": 5,
        "geolocation": None,
        "geolocation_timestamp": None,
        "team_id": "",
        "created": datetime.now(timezone.utc),
    }
    db = get_database()
    try:
        db.players.insert_one(player_doc)
    except DuplicateKeyError as exc:
        if "username" in exc.details.get("keyPattern", {}):
            return "username_taken", None
        return "email_taken", None
    return None, {"player_id": player_id, "access_token": access_token, "refresh_token": refresh_token}

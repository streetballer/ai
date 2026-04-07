from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.player import Player
from src.common.utilities.serialize import public_player, private_player

PRIVATE_PLAYER_PROJECTION = {
    "_id": 1, "username": 1, "email": 1, "email_verified": 1,
    "language": 1, "team_id": 1, "geolocation": 1,
    "google_id": 1, "apple_id": 1, "facebook_id": 1,
}


def get_own_player(player_id: str) -> dict | None:
    db = get_database()
    try:
        doc = db.players.get_one({"_id": ObjectId(player_id)}, PRIVATE_PLAYER_PROJECTION)
    except Exception:
        return None
    if doc is None:
        return None
    return private_player(Player.from_doc(doc))


def get_player_by_id(player_id: str) -> dict | None:
    db = get_database()
    try:
        doc = db.players.get_one({"_id": ObjectId(player_id)}, Player.PUBLIC_PROJECTION)
    except Exception:
        return None
    if doc is None:
        return None
    return public_player(Player.from_doc(doc))

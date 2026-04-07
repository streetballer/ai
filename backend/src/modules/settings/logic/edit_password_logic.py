from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.libraries.hash import hash_value, verify_hash
from src.common.models.player import Player

PLAYER_AUTH_PROJECTION = {"_id": 1, "password_hash": 1}


def edit_password(player_id: str, old_password: str, new_password: str) -> str | None:
    db = get_database()
    try:
        doc = db.players.get_one({"_id": ObjectId(player_id)}, PLAYER_AUTH_PROJECTION)
    except Exception:
        return "not_found"
    if doc is None:
        return "not_found"

    player = Player.from_doc(doc)
    if not verify_hash(old_password, player.password_hash):
        return "wrong_password"

    db.players.update_one(
        {"_id": ObjectId(player_id)},
        {"$set": {"password_hash": hash_value(new_password), "refresh_token_hash": ""}},
    )
    return None

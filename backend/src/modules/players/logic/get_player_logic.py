from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.utilities.serialize import public_player, private_player


def get_own_player(player_id: str) -> dict | None:
    db = get_database()
    try:
        player = db.players.find_one({"_id": ObjectId(player_id)})
    except Exception:
        return None
    if player is None:
        return None
    return private_player(player)


def get_player_by_id(player_id: str) -> dict | None:
    db = get_database()
    try:
        player = db.players.find_one({"_id": ObjectId(player_id)})
    except Exception:
        return None
    if player is None:
        return None
    return public_player(player)

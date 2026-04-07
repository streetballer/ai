from bson import ObjectId
from src.common.libraries.database import get_database, DuplicateEntryError


def edit_username(player_id: str, username: str) -> str | None:
    db = get_database()
    try:
        db.players.update_one({"_id": ObjectId(player_id)}, {"$set": {"username": username}})
    except DuplicateEntryError:
        return "username_taken"
    return None

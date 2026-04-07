from bson import ObjectId
from src.common.libraries.database import get_database


def edit_language(player_id: str, language: str) -> None:
    db = get_database()
    db.players.update_one({"_id": ObjectId(player_id)}, {"$set": {"language": language}})

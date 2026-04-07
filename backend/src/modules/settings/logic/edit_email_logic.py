from bson import ObjectId
from src.common.libraries.database import get_database, DuplicateEntryError


def edit_email(player_id: str, email: str) -> str | None:
    db = get_database()
    try:
        db.players.update_one({"_id": ObjectId(player_id)}, {"$set": {"email": email, "email_verified": False}})
    except DuplicateEntryError:
        return "email_taken"
    return None

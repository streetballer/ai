from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.utilities.serialize import serialize_court


def get_court_by_id(court_id: str) -> dict | None:
    db = get_database()
    try:
        court = db.courts.find_one({"_id": ObjectId(court_id)})
    except Exception:
        return None
    if court is None:
        return None
    return serialize_court(court)

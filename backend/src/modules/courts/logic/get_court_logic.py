from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.court import Court
from src.common.utilities.serialize import serialize_court

COURT_FIELDS_PROJECTION = {"_id": 1, "name": 1, "geolocation": 1, "place_ids": 1}


def get_court_by_id(court_id: str) -> dict | None:
    db = get_database()
    try:
        doc = db.courts.find_one({"_id": ObjectId(court_id)}, COURT_FIELDS_PROJECTION)
    except Exception:
        return None
    if doc is None:
        return None
    return serialize_court(Court.from_doc(doc))

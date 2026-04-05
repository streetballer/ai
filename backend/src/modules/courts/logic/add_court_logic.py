from src.common.libraries.database import get_database
from src.common.utilities.serialize import serialize_court

EARTH_RADIUS_METERS = 6371000
DUPLICATE_RADIUS_METERS = 100
PLACE_SEARCH_RADIUS_METERS = 50000


def _lookup_place_ids(db, lon: float, lat: float) -> list[str]:
    nearest = db.places.find_one({
        "is_parent": False,
        "geolocation": {
            "$nearSphere": {
                "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                "$maxDistance": PLACE_SEARCH_RADIUS_METERS,
            }
        }
    })
    if nearest is None:
        return []
    return [str(nearest["_id"])] + nearest.get("parent_ids", [])


def add_court(lon: float, lat: float, name: str) -> dict | None:
    db = get_database()

    radius_radians = DUPLICATE_RADIUS_METERS / EARTH_RADIUS_METERS
    existing = db.courts.find_one({
        "geolocation": {
            "$geoWithin": {"$centerSphere": [[lon, lat], radius_radians]}
        }
    })
    if existing is not None:
        return None

    place_ids = _lookup_place_ids(db, lon, lat)
    geolocation = {"type": "Point", "coordinates": [lon, lat]}
    result = db.courts.insert_one({
        "name": name,
        "geolocation": geolocation,
        "place_ids": place_ids,
    })

    court = db.courts.find_one({"_id": result.inserted_id})
    return serialize_court(court)

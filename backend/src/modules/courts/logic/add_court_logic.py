from src.common.constants.geo import EARTH_RADIUS_METERS
from src.common.libraries.database import get_database
from src.common.models.court import Court
from src.common.models.place import Place
from src.common.utilities.serialize import serialize_court

DUPLICATE_RADIUS_METERS = 100
PLACE_SEARCH_RADIUS_METERS = 50000

NEAREST_PLACE_PROJECTION = {"_id": 1, "parent_ids": 1}


def _lookup_place_ids(db, lon: float, lat: float) -> list[str]:
    doc = db.places.get_one(
        {
            "is_parent": False,
            "geolocation": {
                "$nearSphere": {
                    "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                    "$maxDistance": PLACE_SEARCH_RADIUS_METERS,
                }
            },
        },
        NEAREST_PLACE_PROJECTION,
    )
    if doc is None:
        return []
    nearest = Place.from_doc(doc)
    return [nearest.id] + nearest.parent_ids


def add_court(lon: float, lat: float, name: str) -> dict | None:
    db = get_database()

    radius_radians = DUPLICATE_RADIUS_METERS / EARTH_RADIUS_METERS
    existing = db.courts.get_one(
        {"geolocation": {"$geoWithin": {"$centerSphere": [[lon, lat], radius_radians]}}},
    )
    if existing is not None:
        return None

    place_ids = _lookup_place_ids(db, lon, lat)
    geolocation = {"type": "Point", "coordinates": [lon, lat]}
    court = Court(name=name, geolocation=geolocation, place_ids=place_ids)
    court.id = db.courts.insert_one(court.to_doc())
    return serialize_court(court)


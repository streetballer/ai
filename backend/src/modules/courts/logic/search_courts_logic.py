from src.common.constants.geo import EARTH_RADIUS_METERS
from src.common.libraries.database import get_database
from src.common.models.court import Court
from src.common.utilities.serialize import serialize_court

DEFAULT_RADIUS_METERS = 10000
COURT_FIELDS_PROJECTION = {"_id": 1, "name": 1, "geolocation": 1, "place_ids": 1}


def search_courts_by_location(lon: float, lat: float, radius: float = DEFAULT_RADIUS_METERS) -> list[dict]:
    db = get_database()
    radius_radians = radius / EARTH_RADIUS_METERS
    docs = db.courts.get_many(
        {"geolocation": {"$geoWithin": {"$centerSphere": [[lon, lat], radius_radians]}}},
        COURT_FIELDS_PROJECTION,
    )
    return [serialize_court(Court.from_doc(doc)) for doc in docs]

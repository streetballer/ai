from src.common.libraries.database import get_database
from src.common.utilities.serialize import serialize_court

EARTH_RADIUS_METERS = 6371000
DEFAULT_RADIUS_METERS = 10000


def search_courts_by_location(lon: float, lat: float, radius: float = DEFAULT_RADIUS_METERS) -> list[dict]:
    db = get_database()
    radius_radians = radius / EARTH_RADIUS_METERS
    courts = db.courts.find({
        "geolocation": {
            "$geoWithin": {"$centerSphere": [[lon, lat], radius_radians]}
        }
    })
    return [serialize_court(c) for c in courts]

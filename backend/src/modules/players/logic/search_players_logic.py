from math import radians, sin, cos, sqrt, atan2
from src.common.libraries.database import get_database
from src.common.utilities.serialize import public_player

EARTH_RADIUS_METERS = 6371000
SEARCH_RADIUS_METERS = 5000
SEARCH_LIMIT = 20


def _distance_meters(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    return EARTH_RADIUS_METERS * 2 * atan2(sqrt(a), sqrt(1 - a))


def search_players_by_location(lon: float, lat: float) -> list[dict]:
    db = get_database()
    radius_radians = SEARCH_RADIUS_METERS / EARTH_RADIUS_METERS
    players = db.players.find({
        "geolocation": {
            "$geoWithin": {"$centerSphere": [[lon, lat], radius_radians]}
        }
    }).limit(SEARCH_LIMIT)
    return [public_player(p) for p in players]


def search_players_by_text(text: str, lon: float | None = None, lat: float | None = None) -> list[dict]:
    db = get_database()
    players = list(db.players.find({"$text": {"$search": text}}).limit(SEARCH_LIMIT))
    results = [public_player(p) for p in players]

    if lon is not None and lat is not None:
        def sort_key(player: dict) -> float:
            geo = next((p.get("geolocation") for p in players if str(p["_id"]) == player["id"]), None)
            if geo and geo.get("coordinates"):
                coords = geo["coordinates"]
                return _distance_meters(lon, lat, coords[0], coords[1])
            return float("inf")

        results.sort(key=sort_key)

    return results

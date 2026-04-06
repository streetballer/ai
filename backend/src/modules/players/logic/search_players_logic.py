from math import radians, sin, cos, sqrt, atan2
from src.common.constants.geo import EARTH_RADIUS_METERS
from src.common.libraries.database import get_database
from src.common.models.player import Player
from src.common.utilities.serialize import public_player

SEARCH_RADIUS_METERS = 5000
SEARCH_LIMIT = 20
PUBLIC_PLAYER_PROJECTION = {"_id": 1, "username": 1, "language": 1, "team_id": 1}
SEARCH_PLAYER_PROJECTION = {"_id": 1, "username": 1, "language": 1, "team_id": 1, "geolocation": 1}


def _distance_meters(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    return EARTH_RADIUS_METERS * 2 * atan2(sqrt(a), sqrt(1 - a))


def search_players_by_location(lon: float, lat: float) -> list[dict]:
    db = get_database()
    radius_radians = SEARCH_RADIUS_METERS / EARTH_RADIUS_METERS
    docs = db.players.find(
        {"geolocation": {"$geoWithin": {"$centerSphere": [[lon, lat], radius_radians]}}},
        PUBLIC_PLAYER_PROJECTION,
    ).limit(SEARCH_LIMIT)
    return [public_player(Player.from_doc(doc)) for doc in docs]


def search_players_by_text(text: str, lon: float | None = None, lat: float | None = None) -> list[dict]:
    db = get_database()
    docs = list(db.players.find({"$text": {"$search": text}}, SEARCH_PLAYER_PROJECTION).limit(SEARCH_LIMIT))
    players = [Player.from_doc(doc) for doc in docs]

    if lon is not None and lat is not None:
        def sort_key(player: Player) -> float:
            if player.geolocation and player.geolocation.get("coordinates"):
                coords = player.geolocation["coordinates"]
                return _distance_meters(lon, lat, coords[0], coords[1])
            return float("inf")

        players.sort(key=sort_key)

    return [public_player(p) for p in players]

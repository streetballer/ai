from src.common.constants.geo import EARTH_RADIUS_METERS
from src.common.libraries.database import get_database
from src.common.models.player import Player
from src.common.utilities.geo import distance_meters
from src.common.utilities.serialize import public_player

SEARCH_RADIUS_METERS = 5000
SEARCH_LIMIT = 20
SEARCH_PLAYER_PROJECTION = {"_id": 1, "username": 1, "language": 1, "team_id": 1, "geolocation": 1}


def search_players_by_location(lon: float, lat: float) -> list[dict]:
    db = get_database()
    radius_radians = SEARCH_RADIUS_METERS / EARTH_RADIUS_METERS
    docs = db.players.get_many(
        {"geolocation": {"$geoWithin": {"$centerSphere": [[lon, lat], radius_radians]}}},
        Player.PUBLIC_PROJECTION,
        limit=SEARCH_LIMIT,
    )
    return [public_player(Player.from_doc(doc)) for doc in docs]


def search_players_by_text(text: str, lon: float | None = None, lat: float | None = None) -> list[dict]:
    db = get_database()
    docs = db.players.get_many({"$text": {"$search": text}}, SEARCH_PLAYER_PROJECTION, limit=SEARCH_LIMIT)
    players = [Player.from_doc(doc) for doc in docs]

    if lon is not None and lat is not None:
        def sort_key(player: Player) -> float:
            if player.geolocation and player.geolocation.get("coordinates"):
                coords = player.geolocation["coordinates"]
                return distance_meters(lon, lat, coords[0], coords[1])
            return float("inf")

        players.sort(key=sort_key)

    return [public_player(p) for p in players]

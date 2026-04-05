from datetime import datetime, timezone
from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.utilities.serialize import serialize_game, serialize_court

EARTH_RADIUS_METERS = 6371000
SEARCH_RADIUS_METERS = 10000


def search_games_by_court(court_id: str) -> dict | None:
    db = get_database()
    try:
        court_doc = db.courts.find_one({"_id": ObjectId(court_id)})
    except Exception:
        return None
    if court_doc is None:
        return None

    now = datetime.now(tz=timezone.utc)
    games = list(db.games.find({
        "court_id": court_id,
        "timestamp": {"$gte": now},
    }))

    return {
        "games": [serialize_game(g) for g in games],
        "courts": [serialize_court(court_doc)],
    }


def search_games_by_location(lon: float, lat: float) -> dict:
    db = get_database()
    radius_radians = SEARCH_RADIUS_METERS / EARTH_RADIUS_METERS
    courts = list(db.courts.find({
        "geolocation": {
            "$geoWithin": {"$centerSphere": [[lon, lat], radius_radians]}
        }
    }))

    if not courts:
        return {"games": [], "courts": []}

    court_ids = [str(c["_id"]) for c in courts]
    now = datetime.now(tz=timezone.utc)
    games = list(db.games.find({
        "court_id": {"$in": court_ids},
        "timestamp": {"$gte": now},
    }))

    courts_with_games = {str(c["_id"]): c for c in courts}
    returned_court_ids = {g["court_id"] for g in games}
    filtered_courts = [courts_with_games[cid] for cid in returned_court_ids if cid in courts_with_games]

    return {
        "games": [serialize_game(g) for g in games],
        "courts": [serialize_court(c) for c in filtered_courts],
    }

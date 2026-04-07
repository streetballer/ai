from datetime import datetime, timezone
from bson import ObjectId
from src.common.constants.geo import EARTH_RADIUS_METERS
from src.common.libraries.database import get_database
from src.common.models.court import Court
from src.common.models.game import Game
from src.common.utilities.serialize import serialize_game, serialize_court

SEARCH_RADIUS_METERS = 10000


def search_games_by_court(court_id: str) -> dict | None:
    db = get_database()
    try:
        court_doc = db.courts.get_one({"_id": ObjectId(court_id)}, Court.FIELDS_PROJECTION)
    except Exception:
        return None
    if court_doc is None:
        return None

    court = Court.from_doc(court_doc)
    now = datetime.now(tz=timezone.utc)
    game_docs = db.games.get_many(
        {"court_id": court_id, "timestamp": {"$gte": now}},
        Game.FIELDS_PROJECTION,
    )
    games = [Game.from_doc(doc) for doc in game_docs]

    return {
        "games": [serialize_game(g) for g in games],
        "courts": [serialize_court(court)],
    }


def search_games_by_location(lon: float, lat: float) -> dict:
    db = get_database()
    radius_radians = SEARCH_RADIUS_METERS / EARTH_RADIUS_METERS
    court_docs = db.courts.get_many(
        {"geolocation": {"$geoWithin": {"$centerSphere": [[lon, lat], radius_radians]}}},
        Court.FIELDS_PROJECTION,
    )

    if not court_docs:
        return {"games": [], "courts": []}

    courts = [Court.from_doc(doc) for doc in court_docs]
    court_ids = [c.id for c in courts]
    now = datetime.now(tz=timezone.utc)
    game_docs = db.games.get_many(
        {"court_id": {"$in": court_ids}, "timestamp": {"$gte": now}},
        Game.FIELDS_PROJECTION,
    )
    games = [Game.from_doc(doc) for doc in game_docs]

    courts_by_id = {c.id: c for c in courts}
    returned_court_ids = {g.court_id for g in games}
    filtered_courts = [courts_by_id[cid] for cid in returned_court_ids if cid in courts_by_id]

    return {
        "games": [serialize_game(g) for g in games],
        "courts": [serialize_court(c) for c in filtered_courts],
    }

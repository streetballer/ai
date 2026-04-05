from datetime import datetime, timezone
from bson import ObjectId
from src.common.libraries.database import get_database


def _floor_to_hour(dt: datetime) -> datetime:
    return dt.replace(minute=0, second=0, microsecond=0)


def create_or_join_game(court_id: str, timestamp: datetime, player_id: str) -> bool:
    db = get_database()
    try:
        db.courts.find_one({"_id": ObjectId(court_id)})
    except Exception:
        return False

    if db.courts.find_one({"_id": ObjectId(court_id)}) is None:
        return False

    game_time = _floor_to_hour(timestamp.astimezone(timezone.utc))

    existing = db.games.find_one({"court_id": court_id, "timestamp": game_time})
    if existing is not None:
        db.games.update_one(
            {"_id": existing["_id"]},
            {"$addToSet": {"player_ids": player_id}},
        )
        return True

    db.games.insert_one({
        "court_id": court_id,
        "timestamp": game_time,
        "player_ids": [player_id],
    })
    return True

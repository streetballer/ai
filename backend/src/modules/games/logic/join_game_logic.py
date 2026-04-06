from datetime import datetime, timezone, timedelta
from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.game import Game

GAME_JOIN_PROJECTION = {"_id": 1, "timestamp": 1}


def join_game(game_id: str, player_id: str) -> str | None:
    """
    Returns None if game not found, "past" if game already started, or "ok" on success.
    """
    db = get_database()
    try:
        doc = db.games.get_one({"_id": ObjectId(game_id)}, GAME_JOIN_PROJECTION)
    except Exception:
        return None

    if doc is None:
        return None

    game = Game.from_doc(doc)
    now = datetime.now(tz=timezone.utc)
    game_time = game.timestamp
    if game_time.tzinfo is None:
        game_time = game_time.replace(tzinfo=timezone.utc)

    if game_time + timedelta(hours=1) <= now:
        return "past"

    db.games.update_one(
        {"_id": ObjectId(game_id)},
        {"$addToSet": {"player_ids": player_id}},
    )
    return "ok"

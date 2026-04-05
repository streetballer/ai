from datetime import datetime, timezone, timedelta
from bson import ObjectId
from src.common.libraries.database import get_database


def join_game(game_id: str, player_id: str) -> str | None:
    """
    Returns None if game not found, "past" if game already started, or "ok" on success.
    """
    db = get_database()
    try:
        game = db.games.find_one({"_id": ObjectId(game_id)})
    except Exception:
        return None

    if game is None:
        return None

    now = datetime.now(tz=timezone.utc)
    game_time = game["timestamp"]
    if game_time.tzinfo is None:
        game_time = game_time.replace(tzinfo=timezone.utc)

    if game_time + timedelta(hours=1) <= now:
        return "past"

    db.games.update_one(
        {"_id": game["_id"]},
        {"$addToSet": {"player_ids": player_id}},
    )
    return "ok"

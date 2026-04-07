from datetime import datetime, timezone
from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.game import Game

def create_or_join_game(court_id: str, timestamp: datetime, player_id: str) -> bool:
    db = get_database()
    try:
        court_doc = db.courts.get_one({"_id": ObjectId(court_id)})
    except Exception:
        return False

    if court_doc is None:
        return False

    game_time = Game.floor_to_hour(timestamp.astimezone(timezone.utc))

    existing_doc = db.games.get_one({"court_id": court_id, "timestamp": game_time})
    if existing_doc is not None:
        existing = Game.from_doc(existing_doc)
        db.games.update_one(
            {"_id": ObjectId(existing.id)},
            {"$addToSet": {"player_ids": player_id}},
        )
        return True

    game = Game(court_id=court_id, timestamp=game_time, player_ids=[player_id])
    db.games.insert_one(game.to_doc())
    return True

from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.player import Player
from src.common.models.score import Score
from src.common.utilities.serialize import public_player, serialize_score

SCORE_FIELDS_PROJECTION = {
    "_id": 1,
    "timestamp": 1,
    "result": 1,
    "points": 1,
    "players": 1,
    "teams": 1,
    "colors": 1,
    "confirmations": 1,
    "rejections": 1,
    "confirmed": 1,
    "player_ids": 1,
    "geolocation": 1,
    "court_id": 1,
    "place_ids": 1,
}
PUBLIC_PLAYER_PROJECTION = {"_id": 1, "username": 1, "language": 1, "team_id": 1}


def get_score(score_id: str) -> dict | None:
    db = get_database()
    try:
        doc = db.scores.find_one({"_id": ObjectId(score_id)}, SCORE_FIELDS_PROJECTION)
    except Exception:
        return None
    if doc is None:
        return None

    score = Score.from_doc(doc)
    player_object_ids = [ObjectId(pid) for pid in score.player_ids if pid]
    player_docs = list(db.players.find({"_id": {"$in": player_object_ids}}, PUBLIC_PLAYER_PROJECTION))
    players = [public_player(Player.from_doc(p)) for p in player_docs]

    return {"score": serialize_score(score), "players": players}

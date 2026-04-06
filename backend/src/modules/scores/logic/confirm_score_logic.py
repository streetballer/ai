from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.score import Score

SCORE_CONFIRM_PROJECTION = {
    "_id": 1,
    "players": 1,
    "player_ids": 1,
    "confirmations": 1,
    "rejections": 1,
    "confirmed": 1,
}


def _side_confirmed(player_ids: list[str], confirmations: list[str]) -> bool:
    if not player_ids:
        return False
    count = sum(1 for pid in player_ids if pid in confirmations)
    return count > len(player_ids) / 2


def confirm_score(score_id: str, player_id: str) -> str | None:
    db = get_database()
    try:
        doc = db.scores.find_one({"_id": ObjectId(score_id)}, SCORE_CONFIRM_PROJECTION)
    except Exception:
        return None
    if doc is None:
        return None

    score = Score.from_doc(doc)

    if player_id not in score.player_ids:
        return "not_in_score"

    if player_id in score.confirmations or player_id in score.rejections:
        return "ok"

    db.scores.update_one(
        {"_id": ObjectId(score_id)},
        {"$addToSet": {"confirmations": player_id}},
    )

    updated_confirmations = score.confirmations + [player_id]
    side_a = list(score.players[0])
    side_b = list(score.players[1])

    if _side_confirmed(side_a, updated_confirmations) and _side_confirmed(side_b, updated_confirmations):
        db.scores.update_one(
            {"_id": ObjectId(score_id)},
            {"$set": {"confirmed": True}},
        )

    return "ok"

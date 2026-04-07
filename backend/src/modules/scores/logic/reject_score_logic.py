from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.score import Score

SCORE_REJECT_PROJECTION = {
    "_id": 1,
    "players": 1,
    "player_ids": 1,
    "rejections": 1,
    "confirmations": 1,
}


def reject_score(score_id: str, player_id: str) -> str | None:
    db = get_database()
    try:
        doc = db.scores.get_one({"_id": ObjectId(score_id)}, SCORE_REJECT_PROJECTION)
    except Exception:
        return None
    if doc is None:
        return None

    score = Score.from_doc(doc)

    if player_id not in score.player_ids:
        return "not_in_score"

    if player_id in score.rejections or player_id in score.confirmations:
        return "ok"

    db.scores.update_one(
        {"_id": ObjectId(score_id)},
        {"$addToSet": {"rejections": player_id}},
    )

    updated_rejections = score.rejections + [player_id]
    side_a = list(score.players[0])
    side_b = list(score.players[1])

    if Score.side_voted(side_a, updated_rejections) or Score.side_voted(side_b, updated_rejections):
        db.scores.delete_one({"_id": ObjectId(score_id)})
        return "deleted"

    return "ok"

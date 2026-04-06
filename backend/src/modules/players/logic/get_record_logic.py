from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.score import Score
from src.modules.players.models.record import Record

PLAYER_EXISTS_PROJECTION = {"_id": 1}
SCORE_FIELDS_PROJECTION = {"_id": 1, "players": 1, "points": 1}


def get_record_with_player(current_player_id: str, target_player_id: str) -> Record | None:
    db = get_database()
    try:
        target_oid = ObjectId(target_player_id)
    except Exception:
        return None

    if db.players.find_one({"_id": target_oid}, PLAYER_EXISTS_PROJECTION) is None:
        return None

    score_docs = list(db.scores.find(
        {"player_ids": {"$all": [current_player_id, target_player_id]}, "confirmed": True},
        SCORE_FIELDS_PROJECTION,
    ))
    scores = [Score.from_doc(doc) for doc in score_docs]

    team_won = 0
    team_lost = 0
    opponents_won = 0
    opponents_lost = 0

    for score in scores:
        current_on_side0 = current_player_id in score.players[0]
        target_on_side0 = target_player_id in score.players[0]
        current_side = 0 if current_on_side0 else 1

        if current_on_side0 == target_on_side0:
            if score.points[current_side] > 0:
                team_won += 1
            else:
                team_lost += 1
        else:
            if score.points[current_side] > 0:
                opponents_won += 1
            else:
                opponents_lost += 1

    return Record(team_won=team_won, team_lost=team_lost, opponents_won=opponents_won, opponents_lost=opponents_lost)

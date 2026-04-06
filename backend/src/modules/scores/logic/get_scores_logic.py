from src.common.libraries.database import get_database
from src.common.models.score import Score
from src.common.utilities.serialize import serialize_score

SCORE_FIELDS_PROJECTION = {
    "_id": 1,
    "timestamp": 1,
    "result": 1,
    "points": 1,
    "players": 1,
    "teams": 1,
    "colors": 1,
    "confirmed": 1,
    "player_ids": 1,
    "court_id": 1,
}


def get_scores(player_id: str, confirmed: bool | None) -> list[dict]:
    db = get_database()
    query: dict = {"player_ids": player_id}
    if confirmed is not None:
        query["confirmed"] = confirmed
    docs = list(db.scores.find(query, SCORE_FIELDS_PROJECTION))
    return [serialize_score(Score.from_doc(doc)) for doc in docs]

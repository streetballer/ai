from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.score import Score

SCORE_FIELDS_PROJECTION = {
    "_id": 1,
    "points": 1,
    "players": 1,
}


def get_league(court_id: str | None, place_id: str | None, team_size: int) -> list[dict] | None:
    db = get_database()

    if court_id:
        try:
            court_doc = db.courts.get_one({"_id": ObjectId(court_id)})
        except Exception:
            return None
        if court_doc is None:
            return None
        location_filter: dict = {"court_id": court_id}
    elif place_id:
        try:
            place_doc = db.places.get_one({"_id": ObjectId(place_id)})
        except Exception:
            return None
        if place_doc is None:
            return None
        location_filter = {"place_ids": place_id}
    else:
        return None

    query = {
        **location_filter,
        "confirmed": True,
        "$expr": {"$eq": [{"$size": {"$arrayElemAt": ["$players", 0]}}, team_size]},
    }
    score_docs = db.scores.get_many(query, SCORE_FIELDS_PROJECTION)
    scores = [Score.from_doc(doc) for doc in score_docs]

    points_by_team: dict[frozenset, int] = {}
    players_by_team: dict[frozenset, list[str]] = {}

    for score in scores:
        for side_idx in range(2):
            side_players = score.players[side_idx]
            side_points = score.points[side_idx]
            key = frozenset(side_players)
            if key not in points_by_team:
                points_by_team[key] = 0
                players_by_team[key] = side_players
            points_by_team[key] += side_points

    standings = sorted(
        [{"players": players_by_team[key], "points": points_by_team[key]} for key in points_by_team],
        key=lambda entry: entry["points"],
        reverse=True,
    )

    return standings

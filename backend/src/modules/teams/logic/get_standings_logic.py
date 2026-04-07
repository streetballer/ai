from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.player import Player
from src.common.models.score import Score
from src.common.models.team import Team
from src.common.utilities.serialize import public_player, serialize_score, serialize_team

PLAYER_TEAM_PROJECTION = {"_id": 1, "team_id": 1}
TEAM_FIELDS_PROJECTION = {"_id": 1, "color": 1, "geolocation": 1, "court_id": 1, "last_activity": 1}
PUBLIC_PLAYER_PROJECTION = {"_id": 1, "username": 1, "language": 1, "team_id": 1}
SCORE_FIELDS_PROJECTION = {"_id": 1, "timestamp": 1, "result": 1, "points": 1, "players": 1, "teams": 1, "colors": 1, "confirmed": 1, "player_ids": 1, "court_id": 1}


def _total_points(team_id: str, scores: list[Score]) -> int:
    total = 0
    for score in scores:
        if score.teams[0] == team_id:
            total += score.points[0]
        elif score.teams[1] == team_id:
            total += score.points[1]
    return total


def get_standings(player_id: str) -> dict | None:
    db = get_database()

    try:
        player_doc = db.players.get_one({"_id": ObjectId(player_id)}, PLAYER_TEAM_PROJECTION)
    except Exception:
        return None
    if player_doc is None:
        return None

    player = Player.from_doc(player_doc)
    if not player.team_id:
        return None

    cutoff = Team.active_cutoff()

    try:
        team_doc = db.teams.get_one(
            {"_id": ObjectId(player.team_id), "last_activity": {"$gte": cutoff}},
            TEAM_FIELDS_PROJECTION,
        )
    except Exception:
        return None
    if team_doc is None:
        return None

    own_team = Team.from_doc(team_doc)

    if not own_team.court_id:
        return None
    team_docs = db.teams.get_many(
        {"court_id": own_team.court_id, "last_activity": {"$gte": cutoff}},
        TEAM_FIELDS_PROJECTION,
    )
    teams = [Team.from_doc(doc) for doc in team_docs]
    team_ids = [t.id for t in teams]

    player_docs = db.players.get_many({"team_id": {"$in": team_ids}}, PUBLIC_PLAYER_PROJECTION)
    players = [public_player(Player.from_doc(p)) for p in player_docs]

    score_docs = db.scores.get_many(
        {"teams": {"$elemMatch": {"$in": team_ids}}, "confirmed": True},
        SCORE_FIELDS_PROJECTION,
    )
    scores = [Score.from_doc(doc) for doc in score_docs]

    teams.sort(key=lambda t: _total_points(t.id, scores), reverse=True)

    return {
        "teams": [serialize_team(t) for t in teams],
        "players": players,
        "scores": [serialize_score(s) for s in scores],
    }

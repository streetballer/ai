from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.player import Player
from src.common.models.team import Team
from src.common.utilities.serialize import public_player, serialize_team

PLAYER_TEAM_PROJECTION = {"_id": 1, "team_id": 1}


def _team_response(db, team: Team) -> dict:
    player_docs = db.players.get_many({"team_id": team.id}, Player.PUBLIC_PROJECTION)
    players = [public_player(Player.from_doc(p)) for p in player_docs]
    return {"team": serialize_team(team), "players": players}


def get_team_by_id(team_id: str) -> dict | None:
    db = get_database()
    try:
        doc = db.teams.get_one({"_id": ObjectId(team_id)}, Team.FIELDS_PROJECTION)
    except Exception:
        return None
    if doc is None:
        return None
    return _team_response(db, Team.from_doc(doc))


def get_team_by_player_id(player_id: str) -> dict | None:
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
    try:
        team_doc = db.teams.get_one(
            {"_id": ObjectId(player.team_id), "last_activity": {"$gte": Team.active_cutoff()}},
            Team.FIELDS_PROJECTION,
        )
    except Exception:
        return None
    if team_doc is None:
        return None
    return _team_response(db, Team.from_doc(team_doc))

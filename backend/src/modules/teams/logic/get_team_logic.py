from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.player import Player
from src.common.models.team import Team
from src.common.utilities.serialize import public_player, serialize_team

TEAM_FIELDS_PROJECTION = {"_id": 1, "color": 1, "geolocation": 1, "court_id": 1, "last_activity": 1}
PUBLIC_PLAYER_PROJECTION = {"_id": 1, "username": 1, "language": 1, "team_id": 1}


def get_team_by_id(team_id: str) -> dict | None:
    db = get_database()
    try:
        doc = db.teams.find_one({"_id": ObjectId(team_id)}, TEAM_FIELDS_PROJECTION)
    except Exception:
        return None
    if doc is None:
        return None

    team = Team.from_doc(doc)
    player_docs = db.players.find({"team_id": team_id}, PUBLIC_PLAYER_PROJECTION)
    players = [public_player(Player.from_doc(p)) for p in player_docs]

    return {"team": serialize_team(team), "players": players}

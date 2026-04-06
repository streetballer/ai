from datetime import datetime, timezone, timedelta
from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.player import Player
from src.common.models.team import Team
from src.common.utilities.serialize import public_player, serialize_team

TEAM_ACTIVE_HOURS = 4
PLAYER_TEAM_PROJECTION = {"_id": 1, "team_id": 1}
TEAM_FIELDS_PROJECTION = {"_id": 1, "color": 1, "geolocation": 1, "court_id": 1, "last_activity": 1}
PUBLIC_PLAYER_PROJECTION = {"_id": 1, "username": 1, "language": 1, "team_id": 1}


def get_own_team(player_id: str) -> dict | None:
    db = get_database()
    try:
        player_doc = db.players.find_one({"_id": ObjectId(player_id)}, PLAYER_TEAM_PROJECTION)
    except Exception:
        return None
    if player_doc is None:
        return None

    player = Player.from_doc(player_doc)
    if not player.team_id:
        return None

    try:
        team_doc = db.teams.find_one({"_id": ObjectId(player.team_id)}, TEAM_FIELDS_PROJECTION)
    except Exception:
        return None
    if team_doc is None:
        db.players.update_one({"_id": player_doc["_id"]}, {"$set": {"team_id": ""}})
        return None

    team = Team.from_doc(team_doc)
    last_activity = team.last_activity
    if last_activity is not None:
        if last_activity.tzinfo is None:
            last_activity = last_activity.replace(tzinfo=timezone.utc)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=TEAM_ACTIVE_HOURS)
        if last_activity < cutoff:
            db.players.update_one({"_id": player_doc["_id"]}, {"$set": {"team_id": ""}})
            return None

    player_docs = db.players.find({"team_id": player.team_id}, PUBLIC_PLAYER_PROJECTION)
    players = [public_player(Player.from_doc(p)) for p in player_docs]

    return {"team": serialize_team(team), "players": players}

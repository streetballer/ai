from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.player import Player
from src.common.models.team import Team
from src.common.utilities.serialize import public_player, serialize_team


def get_team_by_id(team_id: str) -> dict | None:
    db = get_database()
    try:
        doc = db.teams.get_one({"_id": ObjectId(team_id)}, Team.FIELDS_PROJECTION)
    except Exception:
        return None
    if doc is None:
        return None

    team = Team.from_doc(doc)
    player_docs = db.players.get_many({"team_id": team_id}, Player.PUBLIC_PROJECTION)
    players = [public_player(Player.from_doc(p)) for p in player_docs]

    return {"team": serialize_team(team), "players": players}

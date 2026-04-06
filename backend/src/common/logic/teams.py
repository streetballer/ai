from bson import ObjectId
from src.common.models.team import Team

TEAM_FIELDS_PROJECTION = {"_id": 1, "color": 1, "geolocation": 1, "court_id": 1, "last_activity": 1}


def get_active_team(db, team_id: str) -> Team | None:
    if not team_id:
        return None
    try:
        doc = db.teams.get_one({"_id": ObjectId(team_id)}, TEAM_FIELDS_PROJECTION)
    except Exception:
        return None
    if doc is None:
        return None
    team = Team.from_doc(doc)
    return team if team.is_active() else None

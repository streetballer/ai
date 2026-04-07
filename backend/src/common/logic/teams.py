from bson import ObjectId
from src.common.models.team import Team


def get_active_team(db, team_id: str) -> Team | None:
    if not team_id:
        return None
    try:
        doc = db.teams.get_one(
            {"_id": ObjectId(team_id), "last_activity": {"$gte": Team.active_cutoff()}},
            Team.FIELDS_PROJECTION,
        )
    except Exception:
        return None
    if doc is None:
        return None
    return Team.from_doc(doc)

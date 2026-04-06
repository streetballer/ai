from datetime import datetime, timezone, timedelta
from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.court import Court
from src.common.models.player import Player
from src.common.models.team import Team
from src.common.utilities.serialize import serialize_team

TEAM_ACTIVE_HOURS = 4
NEAREST_COURT_MAX_DISTANCE = 10000

PLAYER_TEAM_PROJECTION = {"_id": 1, "team_id": 1, "geolocation": 1}
NEAREST_COURT_PROJECTION = {"_id": 1, "geolocation": 1}
TEAM_EXISTS_PROJECTION = {"_id": 1, "last_activity": 1}


def _get_active_team_id(db, player: Player) -> str | None:
    if not player.team_id:
        return None
    try:
        doc = db.teams.find_one({"_id": ObjectId(player.team_id)}, TEAM_EXISTS_PROJECTION)
    except Exception:
        return None
    if doc is None:
        return None
    last_activity = doc.get("last_activity")
    if last_activity is None:
        return None
    if last_activity.tzinfo is None:
        last_activity = last_activity.replace(tzinfo=timezone.utc)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=TEAM_ACTIVE_HOURS)
    return str(doc["_id"]) if last_activity >= cutoff else None


def _find_nearest_court(db, lon: float, lat: float) -> Court | None:
    doc = db.courts.find_one(
        {
            "geolocation": {
                "$nearSphere": {
                    "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                    "$maxDistance": NEAREST_COURT_MAX_DISTANCE,
                }
            }
        },
        NEAREST_COURT_PROJECTION,
    )
    return Court.from_doc(doc) if doc is not None else None


def create_team(current_player_id: str, target_player_id: str) -> tuple[str | None, dict | None]:
    db = get_database()

    try:
        current_doc = db.players.find_one({"_id": ObjectId(current_player_id)}, PLAYER_TEAM_PROJECTION)
    except Exception:
        return "not_found", None
    if current_doc is None:
        return "not_found", None

    try:
        target_doc = db.players.find_one({"_id": ObjectId(target_player_id)}, PLAYER_TEAM_PROJECTION)
    except Exception:
        return "not_found", None
    if target_doc is None:
        return "not_found", None

    current_player = Player.from_doc(current_doc)
    target_player = Player.from_doc(target_doc)

    if _get_active_team_id(db, current_player) is not None:
        return "already_in_team", None
    if _get_active_team_id(db, target_player) is not None:
        return "target_in_team", None

    geo = current_player.geolocation
    court_id = ""
    geolocation = geo
    if geo and geo.get("coordinates"):
        lon, lat = geo["coordinates"]
        nearest = _find_nearest_court(db, lon, lat)
        if nearest is not None:
            court_id = nearest.id
            geolocation = nearest.geolocation

    now = datetime.now(timezone.utc)
    team = Team(color="#20DFBF", geolocation=geolocation, court_id=court_id, last_activity=now)
    result = db.teams.insert_one(team.to_doc())
    team.id = str(result.inserted_id)

    db.players.update_one({"_id": current_doc["_id"]}, {"$set": {"team_id": team.id}})
    db.players.update_one({"_id": target_doc["_id"]}, {"$set": {"team_id": team.id}})

    return None, serialize_team(team)

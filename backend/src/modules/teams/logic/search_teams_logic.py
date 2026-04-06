from datetime import datetime, timezone, timedelta
from src.common.constants.geo import EARTH_RADIUS_METERS
from src.common.libraries.database import get_database
from src.common.models.team import Team
from src.common.utilities.serialize import serialize_team

SEARCH_RADIUS_METERS = 10000
TEAM_ACTIVE_HOURS = 4


def search_teams_by_court(court_id: str) -> list[dict]:
    db = get_database()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=TEAM_ACTIVE_HOURS)
    docs = db.teams.find(
        {"court_id": court_id, "last_activity": {"$gte": cutoff}},
        {"_id": 1, "color": 1, "geolocation": 1, "court_id": 1, "last_activity": 1},
    )
    return [serialize_team(Team.from_doc(doc)) for doc in docs]


def search_teams_by_location(lon: float, lat: float) -> list[dict]:
    db = get_database()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=TEAM_ACTIVE_HOURS)
    radius_radians = SEARCH_RADIUS_METERS / EARTH_RADIUS_METERS
    docs = db.teams.find(
        {
            "geolocation": {"$geoWithin": {"$centerSphere": [[lon, lat], radius_radians]}},
            "last_activity": {"$gte": cutoff},
        },
        {"_id": 1, "color": 1, "geolocation": 1, "court_id": 1, "last_activity": 1},
    )
    return [serialize_team(Team.from_doc(doc)) for doc in docs]

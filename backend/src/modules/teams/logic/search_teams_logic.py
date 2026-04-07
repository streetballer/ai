from src.common.constants.geo import EARTH_RADIUS_METERS
from src.common.libraries.database import get_database
from src.common.models.team import Team
from src.common.utilities.serialize import serialize_team

SEARCH_RADIUS_METERS = 10000


def search_teams_by_court(court_id: str) -> list[dict]:
    db = get_database()
    cutoff = Team.active_cutoff()
    docs = db.teams.get_many(
        {"court_id": court_id, "last_activity": {"$gte": cutoff}},
        Team.FIELDS_PROJECTION,
    )
    return [serialize_team(Team.from_doc(doc)) for doc in docs]


def search_teams_by_location(lon: float, lat: float) -> list[dict]:
    db = get_database()
    cutoff = Team.active_cutoff()
    radius_radians = SEARCH_RADIUS_METERS / EARTH_RADIUS_METERS
    docs = db.teams.get_many(
        {
            "geolocation": {"$geoWithin": {"$centerSphere": [[lon, lat], radius_radians]}},
            "last_activity": {"$gte": cutoff},
        },
        Team.FIELDS_PROJECTION,
    )
    return [serialize_team(Team.from_doc(doc)) for doc in docs]

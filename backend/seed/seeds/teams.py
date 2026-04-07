from datetime import datetime, timezone, timedelta
from bson import ObjectId
from src.common.libraries.database import Database
from src.common.models.team import Team
from seed.helpers.geo import point
from seed.data.reference import LAT, LON


_TEAM_DEFS = [
    ("#FF4136", point(LON, LAT), 0, timedelta(hours=1)),
    ("#0074D9", point(LON + 0.009, LAT + 0.007), 1, timedelta(hours=2)),
    ("#2ECC40", point(LON + 0.005, LAT + 0.003), 2, timedelta(minutes=30)),
]

_TEAM_MEMBERS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7],
]


def seed_teams(db: Database, court_ids: list[str], player_ids: list[str]) -> list[str]:
    now = datetime.now(timezone.utc)
    team_oids = [ObjectId() for _ in _TEAM_DEFS]
    team_ids = [str(oid) for oid in team_oids]

    docs = []
    for (color, geolocation, court_index, age), team_oid in zip(_TEAM_DEFS, team_oids):
        team = Team(
            color=color,
            geolocation=geolocation,
            court_id=court_ids[court_index],
            last_activity=now - age,
        )
        docs.append({"_id": team_oid, **team.to_doc()})
    db.teams.insert_many(docs)

    for team_id, member_indices in zip(team_ids, _TEAM_MEMBERS):
        member_oids = [ObjectId(player_ids[i]) for i in member_indices]
        db.players.update_many(
            {"_id": {"$in": member_oids}},
            {"$set": {"team_id": team_id}},
        )

    return team_ids

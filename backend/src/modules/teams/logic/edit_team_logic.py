from datetime import datetime, timezone
from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.models.player import Player
from src.common.models.team import Team

TEAM_MIN_PLAYERS = 2
PLAYER_TEAM_PROJECTION = {"_id": 1, "team_id": 1}
TEAM_FIELDS_PROJECTION = {"_id": 1, "color": 1, "geolocation": 1, "court_id": 1, "last_activity": 1}
PLAYER_EXISTS_PROJECTION = {"_id": 1, "team_id": 1}
TEAM_EXISTS_PROJECTION = {"_id": 1, "last_activity": 1}


def _get_active_team(db, player: Player) -> Team | None:
    if not player.team_id:
        return None
    try:
        doc = db.teams.find_one({"_id": ObjectId(player.team_id)}, TEAM_FIELDS_PROJECTION)
    except Exception:
        return None
    if doc is None:
        return None
    team = Team.from_doc(doc)
    return team if team.is_active() else None


def _delete_team(db, team_id: str) -> None:
    db.players.update_many({"team_id": team_id}, {"$set": {"team_id": ""}})
    db.teams.delete_one({"_id": ObjectId(team_id)})


def edit_team(player_id: str, color: str | None, add_player_ids: list[str] | None, remove_player_ids: list[str] | None) -> str | None:
    db = get_database()

    try:
        player_doc = db.players.find_one({"_id": ObjectId(player_id)}, PLAYER_TEAM_PROJECTION)
    except Exception:
        return "not_found"
    if player_doc is None:
        return "not_found"

    player = Player.from_doc(player_doc)
    team = _get_active_team(db, player)
    if team is None:
        return "no_team"

    now = datetime.now(timezone.utc)

    if color is not None:
        db.teams.update_one({"_id": ObjectId(team.id)}, {"$set": {"color": color, "last_activity": now}})

    if add_player_ids:
        try:
            candidate_oids = [ObjectId(pid) for pid in add_player_ids]
        except Exception:
            candidate_oids = []

        candidate_docs = list(db.players.find(
            {"_id": {"$in": candidate_oids}},
            PLAYER_EXISTS_PROJECTION,
        ))
        candidates = [Player.from_doc(d) for d in candidate_docs]

        team_ids_to_check = [p.team_id for p in candidates if p.team_id]
        existing_teams: dict[str, dict] = {}
        if team_ids_to_check:
            for tdoc in db.teams.find(
                {"_id": {"$in": [ObjectId(tid) for tid in team_ids_to_check]}},
                TEAM_EXISTS_PROJECTION,
            ):
                existing_teams[str(tdoc["_id"])] = tdoc

        valid_ids = []
        for raw_doc, player in zip(candidate_docs, candidates):
            if player.team_id:
                tdoc = existing_teams.get(player.team_id)
                if tdoc is not None and Team.from_doc(tdoc).is_active():
                    continue
            valid_ids.append(raw_doc["_id"])

        if valid_ids:
            db.players.update_many({"_id": {"$in": valid_ids}}, {"$set": {"team_id": team.id}})
            db.teams.update_one({"_id": ObjectId(team.id)}, {"$set": {"last_activity": now}})

    if remove_player_ids:
        for pid in remove_player_ids:
            try:
                oid = ObjectId(pid)
            except Exception:
                continue
            db.players.update_one({"_id": oid, "team_id": team.id}, {"$set": {"team_id": ""}})

        remaining = list(db.players.find({"team_id": team.id}, {"_id": 1}))
        if len(remaining) < TEAM_MIN_PLAYERS:
            _delete_team(db, team.id)
        else:
            db.teams.update_one({"_id": ObjectId(team.id)}, {"$set": {"last_activity": now}})

    return None

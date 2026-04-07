from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.libraries.hash import verify_hash
from src.common.logic.teams import get_active_team
from src.common.models.player import Player

PLAYER_AUTH_PROJECTION = {"_id": 1, "password_hash": 1, "team_id": 1}

TEAM_MIN_PLAYERS = 2


def delete_account(player_id: str, password: str) -> str | None:
    db = get_database()
    try:
        doc = db.players.get_one({"_id": ObjectId(player_id)}, PLAYER_AUTH_PROJECTION)
    except Exception:
        return "not_found"
    if doc is None:
        return "not_found"

    player = Player.from_doc(doc)
    if not verify_hash(password, player.password_hash):
        return "wrong_password"

    team = get_active_team(db, player.team_id)
    if team is not None:
        db.players.update_one({"_id": ObjectId(player_id)}, {"$set": {"team_id": ""}})
        remaining = db.players.get_many({"team_id": team.id})
        if len(remaining) < TEAM_MIN_PLAYERS:
            db.players.update_many({"team_id": team.id}, {"$set": {"team_id": ""}})
            db.teams.delete_one({"_id": ObjectId(team.id)})

    db.games.update_many({"player_ids": player_id}, {"$pull": {"player_ids": player_id}})
    db.players.delete_one({"_id": ObjectId(player_id)})
    return None

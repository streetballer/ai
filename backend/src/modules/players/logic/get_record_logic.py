from bson import ObjectId
from src.common.libraries.database import get_database


def get_record_with_player(current_player_id: str, target_player_id: str) -> dict | None:
    db = get_database()
    try:
        target_oid = ObjectId(target_player_id)
    except Exception:
        return None

    if db.players.find_one({"_id": target_oid}) is None:
        return None

    scores = list(db.scores.find({
        "player_ids": {"$all": [current_player_id, target_player_id]},
        "confirmed": True,
    }))

    team_won = 0
    team_lost = 0
    opponents_won = 0
    opponents_lost = 0

    for score in scores:
        players_sides = score.get("players", [[], []])
        points = score.get("points", [0, 0])

        current_on_side0 = current_player_id in players_sides[0]
        target_on_side0 = target_player_id in players_sides[0]
        current_side = 0 if current_on_side0 else 1

        if current_on_side0 == target_on_side0:
            # Teammates: same side
            if points[current_side] > 0:
                team_won += 1
            else:
                team_lost += 1
        else:
            # Opponents: different sides
            if points[current_side] > 0:
                opponents_won += 1
            else:
                opponents_lost += 1

    return {
        "team": {"won": team_won, "lost": team_lost},
        "opponents": {"won": opponents_won, "lost": opponents_lost},
    }

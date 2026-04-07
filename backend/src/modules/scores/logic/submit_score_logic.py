from datetime import datetime, timezone
from bson import ObjectId
from src.common.libraries.database import get_database
from src.common.logic.teams import get_active_team
from src.common.models.court import Court
from src.common.models.player import Player
from src.common.models.score import Score
from src.common.models.team import Team
from src.common.utilities.serialize import serialize_score

PLAYER_INFO_PROJECTION = {"_id": 1, "team_id": 1, "rating": 1}
COURT_PLACES_PROJECTION = {"_id": 1, "place_ids": 1}
TEAM_PLAYERS_PROJECTION = {"_id": 1, "rating": 1, "team_id": 1}


def _get_both_team_players(db, team_id_a: str, team_id_b: str) -> tuple[list[Player], list[Player]]:
    docs = db.players.get_many({"team_id": {"$in": [team_id_a, team_id_b]}}, TEAM_PLAYERS_PROJECTION)
    players_a = [Player.from_doc(d) for d in docs if d.get("team_id") == team_id_a]
    players_b = [Player.from_doc(d) for d in docs if d.get("team_id") == team_id_b]
    return players_a, players_b


def submit_score(
    player_id: str,
    score_1: int,
    score_2: int,
    opponent_id: str,
) -> tuple[str | None, dict | None]:
    db = get_database()

    try:
        player_docs = db.players.get_many(
            {"_id": {"$in": [ObjectId(player_id), ObjectId(opponent_id)]}},
            PLAYER_INFO_PROJECTION,
        )
    except Exception:
        return "player_not_found", None

    docs_by_id = {str(d["_id"]): d for d in player_docs}
    player_doc = docs_by_id.get(player_id)
    opponent_doc = docs_by_id.get(opponent_id)

    if player_doc is None:
        return "player_not_found", None
    if opponent_doc is None:
        return "opponent_not_found", None

    current_player = Player.from_doc(player_doc)
    team_a = get_active_team(db, current_player.team_id)
    if team_a is None:
        return "no_active_team", None

    opponent = Player.from_doc(opponent_doc)
    team_b = get_active_team(db, opponent.team_id)
    if team_b is None:
        return "opponent_no_active_team", None

    if team_a.id == team_b.id:
        return "same_team", None

    players_a, players_b = _get_both_team_players(db, team_a.id, team_b.id)
    player_ids_a = [p.id for p in players_a]
    player_ids_b = [p.id for p in players_b]

    side_a_wins = score_1 > score_2
    winner_players = players_a if side_a_wins else players_b
    loser_players = players_b if side_a_wins else players_a

    winner_avg = sum(p.rating for p in winner_players) / len(winner_players) if winner_players else 5.0
    loser_avg = sum(p.rating for p in loser_players) / len(loser_players) if loser_players else 5.0

    winner_points = Score.calculate_winner_points(winner_avg, loser_avg)
    points_a = winner_points if side_a_wins else 0
    points_b = winner_points if not side_a_wins else 0

    if winner_avg <= loser_avg:
        winner_ids = [p.id for p in winner_players]
        loser_ids = [p.id for p in loser_players]
        db.players.update_many(
            {"_id": {"$in": [ObjectId(pid) for pid in winner_ids]}},
            [{"$set": {"rating": {"$min": [9, {"$add": ["$rating", 1]}]}}}],
        )
        db.players.update_many(
            {"_id": {"$in": [ObjectId(pid) for pid in loser_ids]}},
            [{"$set": {"rating": {"$max": [1, {"$subtract": ["$rating", 1]}]}}}],
        )

    place_ids: list[str] = []
    court_id = team_a.court_id
    if court_id:
        try:
            court_doc = db.courts.get_one({"_id": ObjectId(court_id)}, COURT_PLACES_PROJECTION)
        except Exception:
            court_doc = None
        if court_doc is not None:
            place_ids = Court.from_doc(court_doc).place_ids

    now = datetime.now(timezone.utc)
    confirmations = [player_id]

    score = Score(
        timestamp=now,
        result=(score_1, score_2),
        points=(points_a, points_b),
        players=(player_ids_a, player_ids_b),
        teams=(team_a.id, team_b.id),
        colors=(team_a.color, team_b.color),
        confirmations=confirmations,
        rejections=[],
        confirmed=False,
        player_ids=player_ids_a + player_ids_b,
        geolocation=team_a.geolocation,
        court_id=court_id,
        place_ids=place_ids,
    )

    if Score.side_voted(player_ids_a, confirmations) and Score.side_voted(player_ids_b, confirmations):
        score.confirmed = True

    db.teams.update_many(
        {"_id": {"$in": [ObjectId(team_a.id), ObjectId(team_b.id)]}},
        {"$set": {"last_activity": now}},
    )

    score.id = db.scores.insert_one(score.to_doc())

    return None, serialize_score(score)

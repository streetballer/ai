from datetime import datetime, timezone, timedelta
from src.common.libraries.database import Database
from src.common.models.score import Score


_TEAM_COLORS = ["#FF4136", "#0074D9", "#2ECC40"]

_TEAM_MEMBERS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7],
]

_SCORE_DEFS = [
    (3, 0, 1, 21, 15, 0),
    (2, 1, 2, 21, 10, 1),
    (4, 0, 2, 18, 21, 2),
    (1, 0, 1, 21, 14, 0),
    (5, 1, 2, 21, 19, 1),
    (6, 0, 1, 15, 21, 1),
]


def seed_scores(
    db: Database,
    court_ids: list[str],
    player_ids: list[str],
    team_ids: list[str],
    place_ids: list[str],
) -> list[str]:
    now = datetime.now(timezone.utc)
    docs = []
    for days_ago, team_a_index, team_b_index, score_a, score_b, court_index in _SCORE_DEFS:
        side_a = [player_ids[i] for i in _TEAM_MEMBERS[team_a_index]]
        side_b = [player_ids[i] for i in _TEAM_MEMBERS[team_b_index]]
        all_players = side_a + side_b
        side_a_wins = score_a > score_b
        winner_points = 5
        score = Score(
            timestamp=now - timedelta(days=days_ago),
            result=(score_a, score_b),
            points=(winner_points if side_a_wins else 0, winner_points if not side_a_wins else 0),
            players=(side_a, side_b),
            teams=(team_ids[team_a_index], team_ids[team_b_index]),
            colors=(_TEAM_COLORS[team_a_index], _TEAM_COLORS[team_b_index]),
            confirmations=all_players,
            rejections=[],
            confirmed=True,
            player_ids=all_players,
            geolocation=None,
            court_id=court_ids[court_index],
            place_ids=[place_ids[0]],
        )
        docs.append(score.to_doc())
    return db.scores.insert_many(docs)

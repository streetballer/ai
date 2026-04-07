from datetime import datetime, timezone, timedelta
from src.common.libraries.database import Database
from src.common.models.game import Game


_GAME_DEFS = [
    (1, 0, [0, 1, 2, 3]),
    (1, 1, [3, 4, 5, 6, 7]),
    (2, 2, [0, 1, 2, 6, 7]),
    (3, 3, [0, 1, 3, 4, 5]),
]


def seed_games(db: Database, court_ids: list[str], player_ids: list[str]) -> list[str]:
    now = datetime.now(timezone.utc)
    docs = []
    for days_ahead, court_index, player_indices in _GAME_DEFS:
        timestamp = Game.floor_to_hour(now + timedelta(days=days_ahead)).replace(hour=18)
        game = Game(
            timestamp=timestamp,
            court_id=court_ids[court_index],
            player_ids=[player_ids[i] for i in player_indices],
        )
        docs.append(game.to_doc())
    return db.games.insert_many(docs)

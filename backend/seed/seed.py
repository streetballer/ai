from pymongo import MongoClient
from src.common.environment.config import MONGODB_URI, MONGODB_NAME
from src.common.libraries.database import get_database
from seed.seeds.places import seed_places
from seed.seeds.courts import seed_courts
from seed.seeds.players import seed_players
from seed.seeds.teams import seed_teams
from seed.seeds.games import seed_games
from seed.seeds.scores import seed_scores

_COLLECTIONS = ["places", "courts", "players", "teams", "games", "scores"]


def _clear(db_raw) -> None:
    for collection in _COLLECTIONS:
        db_raw[collection].delete_many({})
    print("Cleared collections.")


def main() -> None:
    client = MongoClient(MONGODB_URI)
    db_raw = client[MONGODB_NAME]
    _clear(db_raw)
    client.close()

    db = get_database()

    place_ids = seed_places(db)
    print(f"Seeded {len(place_ids)} places.")

    court_ids = seed_courts(db, place_ids)
    print(f"Seeded {len(court_ids)} courts.")

    player_ids = seed_players(db)
    print(f"Seeded {len(player_ids)} players.")

    team_ids = seed_teams(db, court_ids, player_ids)
    print(f"Seeded {len(team_ids)} teams.")

    game_ids = seed_games(db, court_ids, player_ids)
    print(f"Seeded {len(game_ids)} games.")

    score_ids = seed_scores(db, court_ids, player_ids, team_ids, place_ids)
    print(f"Seeded {len(score_ids)} scores.")

    print("Done.")


if __name__ == "__main__":
    main()

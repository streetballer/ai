from pymongo import MongoClient, ASCENDING
from pymongo.database import Database
from src.common.environment.config import MONGODB_URI, MONGODB_NAME

_client: MongoClient | None = None


def get_database() -> Database:
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI)
    return _client[MONGODB_NAME]


def setup_indexes() -> None:
    db = get_database()
    db.players.create_index("username", unique=True)
    db.players.create_index("email", unique=True)
    db.players.create_index([("geolocation", "2dsphere")], sparse=True)
    db.players.create_index([("username", "text")])
    db.courts.create_index([("geolocation", "2dsphere")])
    db.games.create_index("court_id")
    db.games.create_index("timestamp")
    db.scores.create_index("player_ids")
    db.places.create_index([("geolocation", "2dsphere")])
    db.places.create_index([("address", "text")])


def close_database() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None

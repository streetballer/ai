from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as _DuplicateKeyError
from src.common.environment.config import MONGODB_URI, MONGODB_NAME
from typing import Any

_client: MongoClient | None = None


class DuplicateEntryError(Exception):
    def __init__(self, key: str) -> None:
        self.key = key


class Collection:
    def __init__(self, collection: Any) -> None:
        self._collection = collection

    def get_one(self, filter: dict[str, Any], projection: dict[str, Any] = {"_id": 1}) -> dict[str, Any] | None:
        return self._collection.find_one(filter, projection)

    def get_many(self, filter: dict[str, Any], projection: dict[str, Any] = {"_id": 1}, limit: int | None = None) -> list[dict[str, Any]]:
        cursor = self._collection.find(filter, projection)
        if limit is not None:
            cursor = cursor.limit(limit)
        return list(cursor)

    def insert_one(self, document: dict[str, Any]) -> str:
        try:
            result = self._collection.insert_one(document)
            return str(result.inserted_id)
        except _DuplicateKeyError as exc:
            key = next(iter(exc.details.get("keyPattern", {})), "")
            raise DuplicateEntryError(key) from exc

    def update_one(self, filter: dict[str, Any], update: dict[str, Any] | list) -> None:
        self._collection.update_one(filter, update)

    def update_many(self, filter: dict[str, Any], update: dict[str, Any] | list) -> None:
        self._collection.update_many(filter, update)

    def delete_one(self, filter: dict[str, Any]) -> None:
        self._collection.delete_one(filter)


class Database:
    def __init__(self, db: Any) -> None:
        self._db = db

    def __getattr__(self, name: str) -> Collection:
        return Collection(getattr(self._db, name))


def _get_raw_db() -> Any:
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI)
    return _client[MONGODB_NAME]


def get_database() -> Database:
    return Database(_get_raw_db())


def setup_indexes() -> None:
    db = _get_raw_db()
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

from pymongo import MongoClient
from pymongo.database import Database
from src.common.environment.config import MONGODB_URI, MONGODB_NAME

_client: MongoClient | None = None


def get_database() -> Database:
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI)
    return _client[MONGODB_NAME]


def close_database() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None

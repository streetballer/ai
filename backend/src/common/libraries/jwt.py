from datetime import datetime, timezone, timedelta
import jwt
from src.common.environment.config import JWT_SECRET, JWT_ACCESS_TTL, JWT_REFRESH_TTL


def create_access_token(player_id: str) -> str:
    payload = {
        "sub": player_id,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(seconds=JWT_ACCESS_TTL),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def create_refresh_token(player_id: str) -> str:
    payload = {
        "sub": player_id,
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(seconds=JWT_REFRESH_TTL),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None

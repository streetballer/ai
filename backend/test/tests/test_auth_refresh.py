from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch
import jwt
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.common.environment.config import JWT_SECRET
from src.common.libraries.hash import hash_value

client = TestClient(app)


def make_token(player_id: str, token_type: str, expired: bool = False) -> str:
    exp = datetime.now(timezone.utc) + timedelta(seconds=-1 if expired else 2419200)
    payload = {"sub": player_id, "type": token_type, "exp": exp}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def mock_db_with_player(player_id: str, refresh_token: str) -> MagicMock:
    db = MagicMock()
    db.players.find_one.return_value = {
        "_id": player_id,
        "refresh_token_hash": hash_value(refresh_token),
    }
    return db


def test_refresh_returns_200_with_new_tokens():
    token = make_token("player_123", "refresh")
    mock_db = mock_db_with_player("player_123", token)
    with patch("src.modules.auth.logic.token_logic.get_database", return_value=mock_db):
        response = client.post(f"/auth/refresh/{token}")
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body["data"]
    assert "refresh_token" in body["data"]


def test_refresh_updates_stored_token_hash():
    token = make_token("player_123", "refresh")
    mock_db = mock_db_with_player("player_123", token)
    with patch("src.modules.auth.logic.token_logic.get_database", return_value=mock_db):
        client.post(f"/auth/refresh/{token}")
    mock_db.players.update_one.assert_called_once()


def test_refresh_returns_498_for_expired_token():
    token = make_token("player_123", "refresh", expired=True)
    response = client.post(f"/auth/refresh/{token}")
    assert response.status_code == 498


def test_refresh_returns_498_for_invalid_token():
    response = client.post("/auth/refresh/not-a-valid-token")
    assert response.status_code == 498


def test_refresh_returns_498_for_access_token_type():
    token = make_token("player_123", "access")
    response = client.post(f"/auth/refresh/{token}")
    assert response.status_code == 498


def test_refresh_returns_498_for_hash_mismatch():
    token = make_token("player_123", "refresh")
    mock_db = mock_db_with_player("player_123", "different_token")
    with patch("src.modules.auth.logic.token_logic.get_database", return_value=mock_db):
        response = client.post(f"/auth/refresh/{token}")
    assert response.status_code == 498


def test_refresh_returns_498_for_unknown_player():
    token = make_token("player_unknown", "refresh")
    mock_db = MagicMock()
    mock_db.players.find_one.return_value = None
    with patch("src.modules.auth.logic.token_logic.get_database", return_value=mock_db):
        response = client.post(f"/auth/refresh/{token}")
    assert response.status_code == 498

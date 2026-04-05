from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from src.main import app
from src.common.libraries.hash import hash_value

client = TestClient(app)

PASSWORD = "password123"


def mock_db_with_player(by_username: bool = True) -> MagicMock:
    db = MagicMock()
    player = {"_id": "player_123", "password_hash": hash_value(PASSWORD)}
    db.players.find_one.return_value = player
    return db


def mock_db_no_player() -> MagicMock:
    db = MagicMock()
    db.players.find_one.return_value = None
    return db


def test_log_in_with_username_returns_200():
    mock_db = mock_db_with_player()
    with patch("src.modules.auth.logic.log_in_logic.get_database", return_value=mock_db):
        response = client.post("/auth/log-in", json={"username": "streetballer", "password": PASSWORD})
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body["data"]
    assert "refresh_token" in body["data"]


def test_log_in_with_email_returns_200():
    mock_db = mock_db_with_player()
    with patch("src.modules.auth.logic.log_in_logic.get_database", return_value=mock_db):
        response = client.post("/auth/log-in", json={"email": "player@example.com", "password": PASSWORD})
    assert response.status_code == 200


def test_log_in_updates_refresh_token_hash():
    mock_db = mock_db_with_player()
    with patch("src.modules.auth.logic.log_in_logic.get_database", return_value=mock_db):
        client.post("/auth/log-in", json={"username": "streetballer", "password": PASSWORD})
    mock_db.players.update_one.assert_called_once()


def test_log_in_returns_401_for_wrong_password():
    mock_db = mock_db_with_player()
    with patch("src.modules.auth.logic.log_in_logic.get_database", return_value=mock_db):
        response = client.post("/auth/log-in", json={"username": "streetballer", "password": "wrongpassword"})
    assert response.status_code == 401


def test_log_in_returns_401_for_unknown_user():
    mock_db = mock_db_no_player()
    with patch("src.modules.auth.logic.log_in_logic.get_database", return_value=mock_db):
        response = client.post("/auth/log-in", json={"username": "nobody", "password": PASSWORD})
    assert response.status_code == 401


def test_log_in_returns_422_when_no_identifier():
    response = client.post("/auth/log-in", json={"password": PASSWORD})
    assert response.status_code == 422


def test_log_in_returns_422_when_missing_password():
    response = client.post("/auth/log-in", json={"username": "streetballer"})
    assert response.status_code == 422

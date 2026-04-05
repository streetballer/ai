from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch
import jwt
from fastapi.testclient import TestClient
from src.main import app
from src.common.environment.config import JWT_SECRET

client = TestClient(app)


def make_token(player_id: str, token_type: str, expired: bool = False) -> str:
    exp = datetime.now(timezone.utc) + timedelta(seconds=-1 if expired else 3600)
    return jwt.encode({"sub": player_id, "type": token_type, "exp": exp}, JWT_SECRET, algorithm="HS256")


def mock_db_with_player(player_id: str) -> MagicMock:
    db = MagicMock()
    db.players.find_one.return_value = {"_id": player_id, "email": "player@example.com", "username": "streetballer"}
    return db


def mock_db_no_player() -> MagicMock:
    db = MagicMock()
    db.players.find_one.return_value = None
    return db


def test_request_reset_returns_200_for_existing_user():
    mock_db = mock_db_with_player("player_123")
    with patch("src.modules.auth.logic.password_logic.get_database", return_value=mock_db):
        with patch("src.modules.auth.logic.password_logic.send_email"):
            response = client.post("/auth/password", json={"username": "streetballer"})
    assert response.status_code == 200


def test_request_reset_returns_200_for_unknown_user():
    mock_db = mock_db_no_player()
    with patch("src.modules.auth.logic.password_logic.get_database", return_value=mock_db):
        response = client.post("/auth/password", json={"username": "nobody"})
    assert response.status_code == 200


def test_request_reset_sends_email_for_existing_user():
    mock_db = mock_db_with_player("player_123")
    with patch("src.modules.auth.logic.password_logic.get_database", return_value=mock_db):
        with patch("src.modules.auth.logic.password_logic.send_email") as mock_send:
            client.post("/auth/password", json={"email": "player@example.com"})
    mock_send.assert_called_once()


def test_request_reset_skips_email_for_unknown_user():
    mock_db = mock_db_no_player()
    with patch("src.modules.auth.logic.password_logic.get_database", return_value=mock_db):
        with patch("src.modules.auth.logic.password_logic.send_email") as mock_send:
            client.post("/auth/password", json={"username": "nobody"})
    mock_send.assert_not_called()


def test_request_reset_returns_422_with_no_identifier():
    response = client.post("/auth/password", json={})
    assert response.status_code == 422


def test_do_reset_returns_200_with_valid_token():
    token = make_token("player_123", "password_reset")
    mock_db = MagicMock()
    with patch("src.modules.auth.logic.password_logic.get_database", return_value=mock_db):
        response = client.post(f"/auth/password/{token}", json={"password": "newpassword123"})
    assert response.status_code == 200


def test_do_reset_clears_refresh_token_hash():
    token = make_token("player_123", "password_reset")
    mock_db = MagicMock()
    with patch("src.modules.auth.logic.password_logic.get_database", return_value=mock_db):
        client.post(f"/auth/password/{token}", json={"password": "newpassword123"})
    call_args = mock_db.players.update_one.call_args
    assert call_args[0][1]["$set"]["refresh_token_hash"] == ""


def test_do_reset_returns_498_for_expired_token():
    token = make_token("player_123", "password_reset", expired=True)
    response = client.post(f"/auth/password/{token}", json={"password": "newpassword123"})
    assert response.status_code == 498


def test_do_reset_returns_498_for_wrong_token_type():
    token = make_token("player_123", "email_verification")
    response = client.post(f"/auth/password/{token}", json={"password": "newpassword123"})
    assert response.status_code == 498


def test_do_reset_returns_422_for_short_password():
    token = make_token("player_123", "password_reset")
    response = client.post(f"/auth/password/{token}", json={"password": "short"})
    assert response.status_code == 422

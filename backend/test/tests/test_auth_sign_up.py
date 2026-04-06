from bson import ObjectId
from unittest.mock import MagicMock, patch
from src.common.libraries.database import DuplicateEntryError
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

VALID_BODY = {"username": "streetballer", "email": "player@example.com", "password": "password123"}


def mock_db_insert_success() -> MagicMock:
    db = MagicMock()
    db.players.insert_one.return_value = str(ObjectId())
    return db


def mock_db_insert_duplicate(field: str) -> MagicMock:
    db = MagicMock()
    db.players.insert_one.side_effect = DuplicateEntryError(field)
    return db


def test_sign_up_returns_200_with_tokens():
    mock_db = mock_db_insert_success()
    with patch("src.modules.auth.logic.sign_up_logic.get_database", return_value=mock_db):
        response = client.post("/auth/sign-up", json=VALID_BODY)
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body["data"]
    assert "refresh_token" in body["data"]


def test_sign_up_returns_409_for_duplicate_username():
    mock_db = mock_db_insert_duplicate("username")
    with patch("src.modules.auth.logic.sign_up_logic.get_database", return_value=mock_db):
        response = client.post("/auth/sign-up", json=VALID_BODY)
    assert response.status_code == 409
    assert "username" in response.json()["message"].lower()


def test_sign_up_returns_409_for_duplicate_email():
    mock_db = mock_db_insert_duplicate("email")
    with patch("src.modules.auth.logic.sign_up_logic.get_database", return_value=mock_db):
        response = client.post("/auth/sign-up", json=VALID_BODY)
    assert response.status_code == 409
    assert "email" in response.json()["message"].lower()


def test_sign_up_returns_422_for_missing_fields():
    response = client.post("/auth/sign-up", json={})
    assert response.status_code == 422


def test_sign_up_returns_422_for_invalid_email():
    body = {**VALID_BODY, "email": "not-an-email"}
    response = client.post("/auth/sign-up", json=body)
    assert response.status_code == 422


def test_sign_up_returns_422_for_short_password():
    body = {**VALID_BODY, "password": "short"}
    response = client.post("/auth/sign-up", json=body)
    assert response.status_code == 422


def test_sign_up_returns_422_for_invalid_username():
    body = {**VALID_BODY, "username": "ab"}
    response = client.post("/auth/sign-up", json=body)
    assert response.status_code == 422

from unittest.mock import MagicMock, patch
from bson import ObjectId
from fastapi.testclient import TestClient
from src.main import app
from src.common.libraries.jwt import create_access_token
from src.common.libraries.hash import hash_value

client = TestClient(app)

PLAYER_ID = str(ObjectId())
TEAM_ID = str(ObjectId())
AUTH_HEADERS = {"Authorization": f"Bearer {create_access_token(PLAYER_ID)}"}

PASSWORD = "securepassword123"
PASSWORD_HASH = hash_value(PASSWORD)

PLAYER_DOC = {
    "_id": ObjectId(PLAYER_ID),
    "password_hash": PASSWORD_HASH,
    "team_id": "",
}

PLAYER_WITH_TEAM_DOC = {
    "_id": ObjectId(PLAYER_ID),
    "password_hash": PASSWORD_HASH,
    "team_id": TEAM_ID,
}

from datetime import datetime, timezone, timedelta

ACTIVE_TEAM_DOC = {
    "_id": ObjectId(TEAM_ID),
    "color": "#FF0000",
    "geolocation": {"type": "Point", "coordinates": [-118.25, 34.05]},
    "court_id": str(ObjectId()),
    "last_activity": datetime.now(timezone.utc) - timedelta(hours=1),
}


# --- POST /settings/username ---

def test_edit_username_returns_200():
    mock_db = MagicMock()
    with patch("src.modules.settings.logic.edit_username_logic.get_database", return_value=mock_db):
        response = client.post("/settings/username", json={"username": "newname"}, headers=AUTH_HEADERS)
    assert response.status_code == 200
    mock_db.players.update_one.assert_called_once()


def test_edit_username_returns_401_without_auth():
    response = client.post("/settings/username", json={"username": "newname"})
    assert response.status_code in (401, 403)


def test_edit_username_returns_422_when_invalid():
    response = client.post("/settings/username", json={"username": "x"}, headers=AUTH_HEADERS)
    assert response.status_code == 422


def test_edit_username_returns_409_when_taken():
    from src.common.libraries.database import DuplicateEntryError
    mock_db = MagicMock()
    mock_db.players.update_one.side_effect = DuplicateEntryError(key="username")
    with patch("src.modules.settings.logic.edit_username_logic.get_database", return_value=mock_db):
        response = client.post("/settings/username", json={"username": "takenname"}, headers=AUTH_HEADERS)
    assert response.status_code == 409


# --- POST /settings/email ---

def test_edit_email_returns_200():
    mock_db = MagicMock()
    with patch("src.modules.settings.logic.edit_email_logic.get_database", return_value=mock_db):
        response = client.post("/settings/email", json={"email": "new@example.com"}, headers=AUTH_HEADERS)
    assert response.status_code == 200
    mock_db.players.update_one.assert_called_once()


def test_edit_email_returns_401_without_auth():
    response = client.post("/settings/email", json={"email": "new@example.com"})
    assert response.status_code in (401, 403)


def test_edit_email_returns_422_when_invalid():
    response = client.post("/settings/email", json={"email": "not-an-email"}, headers=AUTH_HEADERS)
    assert response.status_code == 422


def test_edit_email_returns_409_when_taken():
    from src.common.libraries.database import DuplicateEntryError
    mock_db = MagicMock()
    mock_db.players.update_one.side_effect = DuplicateEntryError(key="email")
    with patch("src.modules.settings.logic.edit_email_logic.get_database", return_value=mock_db):
        response = client.post("/settings/email", json={"email": "taken@example.com"}, headers=AUTH_HEADERS)
    assert response.status_code == 409


def test_edit_email_resets_email_verified():
    mock_db = MagicMock()
    with patch("src.modules.settings.logic.edit_email_logic.get_database", return_value=mock_db):
        client.post("/settings/email", json={"email": "new@example.com"}, headers=AUTH_HEADERS)
    call_args = mock_db.players.update_one.call_args
    assert call_args[0][1]["$set"]["email_verified"] is False


# --- POST /settings/password ---

def test_edit_password_returns_200():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_DOC
    with patch("src.modules.settings.logic.edit_password_logic.get_database", return_value=mock_db):
        response = client.post(
            "/settings/password",
            json={"old_password": PASSWORD, "new_password": "newpassword123"},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 200
    mock_db.players.update_one.assert_called_once()


def test_edit_password_returns_401_without_auth():
    response = client.post(
        "/settings/password",
        json={"old_password": PASSWORD, "new_password": "newpassword123"},
    )
    assert response.status_code in (401, 403)


def test_edit_password_returns_422_when_old_password_wrong():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_DOC
    with patch("src.modules.settings.logic.edit_password_logic.get_database", return_value=mock_db):
        response = client.post(
            "/settings/password",
            json={"old_password": "wrongpassword", "new_password": "newpassword123"},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 422


def test_edit_password_returns_422_when_new_password_too_short():
    response = client.post(
        "/settings/password",
        json={"old_password": PASSWORD, "new_password": "short"},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 422


def test_edit_password_invalidates_refresh_token():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_DOC
    with patch("src.modules.settings.logic.edit_password_logic.get_database", return_value=mock_db):
        client.post(
            "/settings/password",
            json={"old_password": PASSWORD, "new_password": "newpassword123"},
            headers=AUTH_HEADERS,
        )
    call_args = mock_db.players.update_one.call_args
    assert call_args[0][1]["$set"]["refresh_token_hash"] == ""


# --- POST /settings/language ---

def test_edit_language_returns_200():
    mock_db = MagicMock()
    with patch("src.modules.settings.logic.edit_language_logic.get_database", return_value=mock_db):
        response = client.post("/settings/language", json={"language": "es"}, headers=AUTH_HEADERS)
    assert response.status_code == 200
    mock_db.players.update_one.assert_called_once()


def test_edit_language_returns_401_without_auth():
    response = client.post("/settings/language", json={"language": "es"})
    assert response.status_code in (401, 403)


def test_edit_language_returns_422_when_invalid():
    response = client.post("/settings/language", json={"language": "ENG"}, headers=AUTH_HEADERS)
    assert response.status_code == 422


# --- POST /settings/geolocation ---

def test_edit_geolocation_returns_200():
    mock_db = MagicMock()
    with patch("src.modules.settings.logic.edit_geolocation_logic.get_database", return_value=mock_db):
        response = client.post("/settings/geolocation", json={"lon": -118.25, "lat": 34.05}, headers=AUTH_HEADERS)
    assert response.status_code == 200
    mock_db.players.update_one.assert_called_once()


def test_edit_geolocation_returns_401_without_auth():
    response = client.post("/settings/geolocation", json={"lon": -118.25, "lat": 34.05})
    assert response.status_code in (401, 403)


def test_edit_geolocation_returns_422_when_lon_out_of_range():
    response = client.post("/settings/geolocation", json={"lon": 200.0, "lat": 34.05}, headers=AUTH_HEADERS)
    assert response.status_code == 422


def test_edit_geolocation_returns_422_when_lat_out_of_range():
    response = client.post("/settings/geolocation", json={"lon": -118.25, "lat": 100.0}, headers=AUTH_HEADERS)
    assert response.status_code == 422


def test_edit_geolocation_stores_geojson_point():
    mock_db = MagicMock()
    with patch("src.modules.settings.logic.edit_geolocation_logic.get_database", return_value=mock_db):
        client.post("/settings/geolocation", json={"lon": -118.25, "lat": 34.05}, headers=AUTH_HEADERS)
    call_args = mock_db.players.update_one.call_args
    geolocation = call_args[0][1]["$set"]["geolocation"]
    assert geolocation["type"] == "Point"
    assert geolocation["coordinates"] == [-118.25, 34.05]


# --- POST /settings/delete-account ---

def test_delete_account_returns_200():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_DOC
    with patch("src.modules.settings.logic.delete_account_logic.get_database", return_value=mock_db):
        response = client.post("/settings/delete-account", json={"password": PASSWORD}, headers=AUTH_HEADERS)
    assert response.status_code == 200
    mock_db.players.delete_one.assert_called_once()


def test_delete_account_returns_401_without_auth():
    response = client.post("/settings/delete-account", json={"password": PASSWORD})
    assert response.status_code in (401, 403)


def test_delete_account_returns_422_when_wrong_password():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_DOC
    with patch("src.modules.settings.logic.delete_account_logic.get_database", return_value=mock_db):
        response = client.post("/settings/delete-account", json={"password": "wrongpassword"}, headers=AUTH_HEADERS)
    assert response.status_code == 422


def test_delete_account_removes_from_games():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_DOC
    with patch("src.modules.settings.logic.delete_account_logic.get_database", return_value=mock_db):
        client.post("/settings/delete-account", json={"password": PASSWORD}, headers=AUTH_HEADERS)
    mock_db.games.update_many.assert_called_once()


def test_delete_account_removes_player_from_active_team():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_WITH_TEAM_DOC
    mock_db.teams.get_one.return_value = ACTIVE_TEAM_DOC
    mock_db.players.get_many.return_value = [{"_id": ObjectId()}]
    with patch("src.modules.settings.logic.delete_account_logic.get_database", return_value=mock_db):
        response = client.post("/settings/delete-account", json={"password": PASSWORD}, headers=AUTH_HEADERS)
    assert response.status_code == 200
    mock_db.players.update_one.assert_called()


def test_delete_account_deletes_team_when_below_minimum():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_WITH_TEAM_DOC
    mock_db.teams.get_one.return_value = ACTIVE_TEAM_DOC
    mock_db.players.get_many.return_value = []
    with patch("src.modules.settings.logic.delete_account_logic.get_database", return_value=mock_db):
        response = client.post("/settings/delete-account", json={"password": PASSWORD}, headers=AUTH_HEADERS)
    assert response.status_code == 200
    mock_db.teams.delete_one.assert_called_once()

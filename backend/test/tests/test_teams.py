from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta
from bson import ObjectId
from fastapi.testclient import TestClient
from src.main import app
from src.common.libraries.jwt import create_access_token

client = TestClient(app)

PLAYER_ID = str(ObjectId())
OTHER_PLAYER_ID = str(ObjectId())
TEAM_ID = str(ObjectId())
COURT_ID = str(ObjectId())
AUTH_HEADERS = {"Authorization": f"Bearer {create_access_token(PLAYER_ID)}"}

NOW = datetime.now(timezone.utc)
ACTIVE_LAST_ACTIVITY = NOW - timedelta(hours=1)
INACTIVE_LAST_ACTIVITY = NOW - timedelta(hours=5)

PLAYER_DOC = {
    "_id": ObjectId(PLAYER_ID),
    "username": "streetballer",
    "language": "en",
    "team_id": TEAM_ID,
    "geolocation": {"type": "Point", "coordinates": [-118.25, 34.05]},
}

OTHER_PLAYER_DOC = {
    "_id": ObjectId(OTHER_PLAYER_ID),
    "username": "baller2",
    "language": "en",
    "team_id": "",
    "geolocation": None,
}

TEAM_DOC = {
    "_id": ObjectId(TEAM_ID),
    "color": "#20DFBF",
    "geolocation": {"type": "Point", "coordinates": [-118.25, 34.05]},
    "court_id": COURT_ID,
    "last_activity": ACTIVE_LAST_ACTIVITY,
}

COURT_DOC = {
    "_id": ObjectId(COURT_ID),
    "name": "Venice Beach Court",
    "geolocation": {"type": "Point", "coordinates": [-118.47, 33.98]},
    "place_ids": [],
}


# --- GET /teams ---

def test_search_teams_by_court_returns_200():
    mock_db = MagicMock()
    mock_db.teams.get_many.return_value = [TEAM_DOC]
    with patch("src.modules.teams.logic.search_teams_logic.get_database", return_value=mock_db):
        response = client.get("/teams", params={"court_id": COURT_ID})
    assert response.status_code == 200
    assert "teams" in response.json()["data"]


def test_search_teams_by_location_returns_200():
    mock_db = MagicMock()
    mock_db.teams.get_many.return_value = [TEAM_DOC]
    with patch("src.modules.teams.logic.search_teams_logic.get_database", return_value=mock_db):
        response = client.get("/teams", params={"lon": -118.25, "lat": 34.05})
    assert response.status_code == 200
    assert "teams" in response.json()["data"]


def test_search_teams_returns_422_with_no_params():
    response = client.get("/teams")
    assert response.status_code == 422


def test_search_teams_returns_422_with_only_lon():
    response = client.get("/teams", params={"lon": -118.25})
    assert response.status_code == 422


# --- POST /teams ---

def test_create_team_returns_200():
    mock_db = MagicMock()
    mock_db.players.get_many.return_value = [
        {**PLAYER_DOC, "team_id": ""},
        OTHER_PLAYER_DOC,
    ]
    mock_db.teams.get_one.return_value = None
    mock_db.courts.get_one.return_value = COURT_DOC
    mock_db.teams.insert_one.return_value = TEAM_ID
    with patch("src.modules.teams.logic.create_team_logic.get_database", return_value=mock_db):
        response = client.post("/teams", json={"player_id": OTHER_PLAYER_ID}, headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert "team" in response.json()["data"]


def test_create_team_returns_404_when_target_not_found():
    mock_db = MagicMock()
    mock_db.players.get_many.return_value = [{**PLAYER_DOC, "team_id": ""}]
    with patch("src.modules.teams.logic.create_team_logic.get_database", return_value=mock_db):
        response = client.post("/teams", json={"player_id": OTHER_PLAYER_ID}, headers=AUTH_HEADERS)
    assert response.status_code == 404


def test_create_team_returns_409_when_current_player_in_active_team():
    mock_db = MagicMock()
    mock_db.players.get_many.return_value = [PLAYER_DOC, OTHER_PLAYER_DOC]
    mock_db.teams.get_one.return_value = TEAM_DOC
    with patch("src.modules.teams.logic.create_team_logic.get_database", return_value=mock_db):
        response = client.post("/teams", json={"player_id": OTHER_PLAYER_ID}, headers=AUTH_HEADERS)
    assert response.status_code == 409


def test_create_team_returns_409_when_target_in_active_team():
    mock_db = MagicMock()
    mock_db.players.get_many.return_value = [
        {**PLAYER_DOC, "team_id": ""},
        {**OTHER_PLAYER_DOC, "team_id": TEAM_ID},
    ]
    mock_db.teams.get_one.return_value = TEAM_DOC
    with patch("src.modules.teams.logic.create_team_logic.get_database", return_value=mock_db):
        response = client.post("/teams", json={"player_id": OTHER_PLAYER_ID}, headers=AUTH_HEADERS)
    assert response.status_code == 409


def test_create_team_returns_401_without_auth():
    response = client.post("/teams", json={"player_id": OTHER_PLAYER_ID})
    assert response.status_code in (401, 403)


def test_create_team_returns_422_when_missing_player_id():
    response = client.post("/teams", json={}, headers=AUTH_HEADERS)
    assert response.status_code == 422


# --- GET /teams/team ---

def test_get_own_team_returns_200():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_DOC
    mock_db.teams.get_one.return_value = TEAM_DOC
    mock_db.players.get_many.return_value = [PLAYER_DOC]
    with patch("src.modules.teams.logic.get_own_team_logic.get_database", return_value=mock_db):
        response = client.get("/teams/team", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()["data"]
    assert "team" in data
    assert "players" in data


def test_get_own_team_returns_404_when_player_has_no_team():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = {**PLAYER_DOC, "team_id": ""}
    with patch("src.modules.teams.logic.get_own_team_logic.get_database", return_value=mock_db):
        response = client.get("/teams/team", headers=AUTH_HEADERS)
    assert response.status_code == 404


def test_get_own_team_returns_404_when_team_inactive():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_DOC
    mock_db.teams.get_one.return_value = None
    with patch("src.modules.teams.logic.get_own_team_logic.get_database", return_value=mock_db):
        response = client.get("/teams/team", headers=AUTH_HEADERS)
    assert response.status_code == 404


def test_get_own_team_returns_401_without_auth():
    response = client.get("/teams/team")
    assert response.status_code in (401, 403)


# --- POST /teams/team ---

def test_edit_team_color_returns_200():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_DOC
    mock_db.teams.get_one.return_value = TEAM_DOC
    with patch("src.modules.teams.logic.edit_team_logic.get_database", return_value=mock_db):
        response = client.post("/teams/team", json={"color": "#FF0000"}, headers=AUTH_HEADERS)
    assert response.status_code == 200
    mock_db.teams.update_one.assert_called_once()


def test_edit_team_add_player_returns_200():
    added_player_doc = {**OTHER_PLAYER_DOC, "_id": ObjectId(OTHER_PLAYER_ID), "team_id": ""}
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_DOC
    mock_db.teams.get_one.return_value = TEAM_DOC
    mock_db.players.get_many.return_value = [added_player_doc]
    with patch("src.modules.teams.logic.edit_team_logic.get_database", return_value=mock_db):
        response = client.post("/teams/team", json={"add_player_ids": [OTHER_PLAYER_ID]}, headers=AUTH_HEADERS)
    assert response.status_code == 200


def test_edit_team_remove_player_deletes_team_when_below_minimum():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_DOC
    mock_db.teams.get_one.return_value = TEAM_DOC
    mock_db.players.get_many.return_value = [PLAYER_DOC]
    with patch("src.modules.teams.logic.edit_team_logic.get_database", return_value=mock_db):
        response = client.post("/teams/team", json={"remove_player_ids": [OTHER_PLAYER_ID]}, headers=AUTH_HEADERS)
    assert response.status_code == 200
    mock_db.teams.delete_one.assert_called_once()


def test_edit_team_returns_404_when_no_active_team():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = {**PLAYER_DOC, "team_id": ""}
    with patch("src.modules.teams.logic.edit_team_logic.get_database", return_value=mock_db):
        response = client.post("/teams/team", json={"color": "#FF0000"}, headers=AUTH_HEADERS)
    assert response.status_code == 404


def test_edit_team_returns_401_without_auth():
    response = client.post("/teams/team", json={"color": "#FF0000"})
    assert response.status_code in (401, 403)


def test_edit_team_returns_422_when_no_fields_provided():
    response = client.post("/teams/team", json={}, headers=AUTH_HEADERS)
    assert response.status_code == 422


def test_edit_team_returns_422_for_invalid_color():
    response = client.post("/teams/team", json={"color": "not-a-color"}, headers=AUTH_HEADERS)
    assert response.status_code == 422


# --- GET /teams/standings ---

def test_get_standings_returns_200():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_DOC
    mock_db.teams.get_one.return_value = TEAM_DOC
    mock_db.teams.get_many.return_value = [TEAM_DOC]
    mock_db.players.get_many.return_value = [PLAYER_DOC]
    mock_db.scores.get_many.return_value = []
    with patch("src.modules.teams.logic.get_standings_logic.get_database", return_value=mock_db):
        response = client.get("/teams/standings", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()["data"]
    assert "teams" in data
    assert "players" in data
    assert "scores" in data


def test_get_standings_returns_404_when_no_active_team():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = {**PLAYER_DOC, "team_id": ""}
    with patch("src.modules.teams.logic.get_standings_logic.get_database", return_value=mock_db):
        response = client.get("/teams/standings", headers=AUTH_HEADERS)
    assert response.status_code == 404


def test_get_standings_returns_401_without_auth():
    response = client.get("/teams/standings")
    assert response.status_code in (401, 403)


# --- GET /teams/:team_id ---

def test_get_team_returns_200_by_team_id():
    mock_db = MagicMock()
    mock_db.teams.get_one.return_value = TEAM_DOC
    mock_db.players.get_many.return_value = [PLAYER_DOC]
    with patch("src.modules.teams.logic.get_team_logic.get_database", return_value=mock_db):
        response = client.get(f"/teams/{TEAM_ID}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "team" in data
    assert "players" in data


def test_get_team_returns_200_by_player_id():
    mock_db = MagicMock()
    mock_db.players.get_one.return_value = PLAYER_DOC
    mock_db.teams.get_one.return_value = TEAM_DOC
    mock_db.players.get_many.return_value = [PLAYER_DOC]
    with patch("src.modules.teams.logic.get_team_logic.get_database", return_value=mock_db):
        response = client.get(f"/teams/{PLAYER_ID}?by=player")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "team" in data
    assert "players" in data


def test_get_team_returns_404_when_not_found():
    mock_db = MagicMock()
    mock_db.teams.get_one.return_value = None
    mock_db.players.get_one.return_value = None
    with patch("src.modules.teams.logic.get_team_logic.get_database", return_value=mock_db):
        response = client.get(f"/teams/{TEAM_ID}")
    assert response.status_code == 404

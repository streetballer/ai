from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta
from bson import ObjectId
from fastapi.testclient import TestClient
from src.main import app
from src.common.libraries.jwt import create_access_token

client = TestClient(app)

PLAYER_ID = str(ObjectId())
AUTH_HEADERS = {"Authorization": f"Bearer {create_access_token(PLAYER_ID)}"}
COURT_ID = str(ObjectId())
GAME_ID = str(ObjectId())

def _make_cursor(docs: list) -> MagicMock:
    cursor = MagicMock()
    cursor.limit.return_value = docs
    return cursor


COURT_DOC = {
    "_id": ObjectId(COURT_ID),
    "name": "Venice Beach Court",
    "geolocation": {"type": "Point", "coordinates": [-118.47, 33.98]},
    "place_ids": [],
}

FUTURE_TIME = datetime.now(tz=timezone.utc) + timedelta(hours=2)
FUTURE_TIME = FUTURE_TIME.replace(minute=0, second=0, microsecond=0)

GAME_DOC = {
    "_id": ObjectId(GAME_ID),
    "court_id": COURT_ID,
    "timestamp": FUTURE_TIME,
    "player_ids": [PLAYER_ID],
}


# --- GET /games ---

def test_search_games_by_court_returns_200():
    mock_db = MagicMock()
    mock_db.courts.find_one.return_value = COURT_DOC
    mock_db.games.find.return_value = _make_cursor([GAME_DOC])
    with patch("src.modules.games.logic.search_games_logic.get_database", return_value=mock_db):
        response = client.get("/games", params={"court_id": COURT_ID})
    assert response.status_code == 200
    data = response.json()["data"]
    assert "games" in data
    assert "courts" in data


def test_search_games_by_court_returns_404_when_court_not_found():
    mock_db = MagicMock()
    mock_db.courts.find_one.return_value = None
    with patch("src.modules.games.logic.search_games_logic.get_database", return_value=mock_db):
        response = client.get("/games", params={"court_id": COURT_ID})
    assert response.status_code == 404


def test_search_games_by_location_returns_200():
    mock_db = MagicMock()
    mock_db.courts.find.return_value = _make_cursor([COURT_DOC])
    mock_db.games.find.return_value = _make_cursor([GAME_DOC])
    with patch("src.modules.games.logic.search_games_logic.get_database", return_value=mock_db):
        response = client.get("/games", params={"lon": -118.47, "lat": 33.98})
    assert response.status_code == 200


def test_search_games_returns_422_with_no_params():
    response = client.get("/games")
    assert response.status_code == 422


def test_search_games_returns_422_with_only_lon():
    response = client.get("/games", params={"lon": -118.47})
    assert response.status_code == 422


# --- POST /games ---

def test_create_game_returns_200():
    mock_db = MagicMock()
    mock_db.courts.find_one.return_value = COURT_DOC
    mock_db.games.find_one.return_value = None
    with patch("src.modules.games.logic.create_game_logic.get_database", return_value=mock_db):
        response = client.post(
            "/games",
            json={"court_id": COURT_ID, "timestamp": FUTURE_TIME.isoformat()},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 200


def test_create_game_joins_existing_game():
    mock_db = MagicMock()
    mock_db.courts.find_one.return_value = COURT_DOC
    mock_db.games.find_one.return_value = GAME_DOC
    with patch("src.modules.games.logic.create_game_logic.get_database", return_value=mock_db):
        response = client.post(
            "/games",
            json={"court_id": COURT_ID, "timestamp": FUTURE_TIME.isoformat()},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 200
    mock_db.games.update_one.assert_called_once()


def test_create_game_returns_401_without_auth():
    response = client.post("/games", json={"court_id": COURT_ID, "timestamp": FUTURE_TIME.isoformat()})
    assert response.status_code in (401, 403)


def test_create_game_returns_422_when_court_not_found():
    mock_db = MagicMock()
    mock_db.courts.find_one.return_value = None
    with patch("src.modules.games.logic.create_game_logic.get_database", return_value=mock_db):
        response = client.post(
            "/games",
            json={"court_id": COURT_ID, "timestamp": FUTURE_TIME.isoformat()},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 422


# --- POST /games/:game_id/join ---

def test_join_game_returns_200():
    mock_db = MagicMock()
    mock_db.games.find_one.return_value = GAME_DOC
    with patch("src.modules.games.logic.join_game_logic.get_database", return_value=mock_db):
        response = client.post(f"/games/{GAME_ID}/join", headers=AUTH_HEADERS)
    assert response.status_code == 200
    mock_db.games.update_one.assert_called_once()


def test_join_game_returns_404_when_not_found():
    mock_db = MagicMock()
    mock_db.games.find_one.return_value = None
    with patch("src.modules.games.logic.join_game_logic.get_database", return_value=mock_db):
        response = client.post(f"/games/{GAME_ID}/join", headers=AUTH_HEADERS)
    assert response.status_code == 404


def test_join_game_allows_in_progress_game():
    in_progress_game = {**GAME_DOC, "timestamp": datetime.now(tz=timezone.utc) - timedelta(minutes=30)}
    mock_db = MagicMock()
    mock_db.games.find_one.return_value = in_progress_game
    with patch("src.modules.games.logic.join_game_logic.get_database", return_value=mock_db):
        response = client.post(f"/games/{GAME_ID}/join", headers=AUTH_HEADERS)
    assert response.status_code == 200


def test_join_game_returns_403_for_past_game():
    past_game = {**GAME_DOC, "timestamp": datetime.now(tz=timezone.utc) - timedelta(hours=1, seconds=1)}
    mock_db = MagicMock()
    mock_db.games.find_one.return_value = past_game
    with patch("src.modules.games.logic.join_game_logic.get_database", return_value=mock_db):
        response = client.post(f"/games/{GAME_ID}/join", headers=AUTH_HEADERS)
    assert response.status_code == 403


def test_join_game_returns_401_without_auth():
    response = client.post(f"/games/{GAME_ID}/join")
    assert response.status_code in (401, 403)

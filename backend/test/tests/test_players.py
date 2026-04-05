from unittest.mock import MagicMock, patch
from bson import ObjectId
from fastapi.testclient import TestClient
from src.main import app
from src.common.libraries.jwt import create_access_token

client = TestClient(app)

PLAYER_ID = str(ObjectId())
OTHER_PLAYER_ID = str(ObjectId())
AUTH_HEADERS = {"Authorization": f"Bearer {create_access_token(PLAYER_ID)}"}

PLAYER_DOC = {
    "_id": ObjectId(PLAYER_ID),
    "username": "streetballer",
    "email": "player@example.com",
    "email_verified": True,
    "language": "en",
    "team_id": None,
    "geolocation": {"type": "Point", "coordinates": [-118.25, 34.05]},
    "google_id": None,
    "apple_id": None,
    "facebook_id": None,
    "password_hash": "hash",
    "refresh_token_hash": "hash",
    "rating": 5,
    "geolocation_timestamp": None,
    "created": None,
}


def _make_cursor(docs: list) -> MagicMock:
    cursor = MagicMock()
    cursor.limit.return_value = docs
    return cursor


# --- GET /players ---

def test_search_players_by_location_returns_200():
    mock_db = MagicMock()
    mock_db.players.find.return_value = _make_cursor([PLAYER_DOC])
    with patch("src.modules.players.logic.search_players_logic.get_database", return_value=mock_db):
        response = client.get("/players", params={"lon": -118.25, "lat": 34.05})
    assert response.status_code == 200
    assert "players" in response.json()["data"]


def test_search_players_by_text_returns_200():
    mock_db = MagicMock()
    mock_db.players.find.return_value = _make_cursor([PLAYER_DOC])
    with patch("src.modules.players.logic.search_players_logic.get_database", return_value=mock_db):
        response = client.get("/players", params={"text": "street"})
    assert response.status_code == 200
    assert "players" in response.json()["data"]


def test_search_players_returns_public_fields_only():
    mock_db = MagicMock()
    mock_db.players.find.return_value = _make_cursor([PLAYER_DOC])
    with patch("src.modules.players.logic.search_players_logic.get_database", return_value=mock_db):
        response = client.get("/players", params={"text": "street"})
    player = response.json()["data"]["players"][0]
    assert "id" in player
    assert "username" in player
    assert "language" in player
    assert "email" not in player
    assert "email_verified" not in player
    assert "password_hash" not in player
    assert "refresh_token_hash" not in player
    assert "rating" not in player
    assert "geolocation_timestamp" not in player
    assert "created" not in player


def test_search_players_returns_422_with_no_params():
    response = client.get("/players")
    assert response.status_code == 422


def test_search_players_returns_422_with_only_lon():
    response = client.get("/players", params={"lon": -118.25})
    assert response.status_code == 422


# --- GET /players/player ---

def test_get_own_player_returns_200():
    mock_db = MagicMock()
    mock_db.players.find_one.return_value = PLAYER_DOC
    with patch("src.modules.players.logic.get_player_logic.get_database", return_value=mock_db):
        response = client.get("/players/player", headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert "player" in response.json()["data"]


def test_get_own_player_returns_private_fields():
    mock_db = MagicMock()
    mock_db.players.find_one.return_value = PLAYER_DOC
    with patch("src.modules.players.logic.get_player_logic.get_database", return_value=mock_db):
        response = client.get("/players/player", headers=AUTH_HEADERS)
    player = response.json()["data"]["player"]
    assert "email" in player
    assert "email_verified" in player
    assert "geolocation" in player
    assert "google_id" in player
    assert "password_hash" not in player
    assert "refresh_token_hash" not in player
    assert "rating" not in player
    assert "geolocation_timestamp" not in player
    assert "created" not in player


def test_get_own_player_returns_401_without_auth():
    response = client.get("/players/player")
    assert response.status_code in (401, 403)


def test_get_own_player_returns_404_when_not_found():
    mock_db = MagicMock()
    mock_db.players.find_one.return_value = None
    with patch("src.modules.players.logic.get_player_logic.get_database", return_value=mock_db):
        response = client.get("/players/player", headers=AUTH_HEADERS)
    assert response.status_code == 404


# --- GET /players/:player_id ---

def test_get_player_returns_200():
    mock_db = MagicMock()
    mock_db.players.find_one.return_value = PLAYER_DOC
    with patch("src.modules.players.logic.get_player_logic.get_database", return_value=mock_db):
        response = client.get(f"/players/{PLAYER_ID}")
    assert response.status_code == 200
    assert "player" in response.json()["data"]


def test_get_player_returns_public_fields_only():
    mock_db = MagicMock()
    mock_db.players.find_one.return_value = PLAYER_DOC
    with patch("src.modules.players.logic.get_player_logic.get_database", return_value=mock_db):
        response = client.get(f"/players/{PLAYER_ID}")
    player = response.json()["data"]["player"]
    assert "id" in player
    assert "username" in player
    assert "language" in player
    assert "email" not in player
    assert "email_verified" not in player
    assert "password_hash" not in player
    assert "rating" not in player
    assert "geolocation" not in player
    assert "google_id" not in player


def test_get_player_returns_404_when_not_found():
    mock_db = MagicMock()
    mock_db.players.find_one.return_value = None
    with patch("src.modules.players.logic.get_player_logic.get_database", return_value=mock_db):
        response = client.get(f"/players/{PLAYER_ID}")
    assert response.status_code == 404


# --- GET /players/:player_id/record ---

def _make_opponent_score(current_wins: bool) -> dict:
    """Current player and target player on opposite sides."""
    if current_wins:
        players_sides = [[PLAYER_ID], [OTHER_PLAYER_ID]]
        points = [5, 0]
    else:
        players_sides = [[OTHER_PLAYER_ID], [PLAYER_ID]]
        points = [5, 0]
    return {
        "players": players_sides,
        "points": points,
        "player_ids": [PLAYER_ID, OTHER_PLAYER_ID],
        "confirmed": True,
    }


def _make_teammate_score(team_wins: bool) -> dict:
    """Current player and target player on the same side."""
    opponent_id = str(ObjectId())
    players_sides = [[PLAYER_ID, OTHER_PLAYER_ID], [opponent_id]]
    points = [5, 0] if team_wins else [0, 5]
    return {
        "players": players_sides,
        "points": points,
        "player_ids": [PLAYER_ID, OTHER_PLAYER_ID, opponent_id],
        "confirmed": True,
    }


def test_get_record_returns_200():
    mock_db = MagicMock()
    mock_db.players.find_one.return_value = {"_id": ObjectId(OTHER_PLAYER_ID)}
    mock_db.scores.find.return_value = [_make_opponent_score(True)]
    with patch("src.modules.players.logic.get_record_logic.get_database", return_value=mock_db):
        response = client.get(f"/players/{OTHER_PLAYER_ID}/record", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()["data"]
    assert "team" in data
    assert "opponents" in data


def test_get_record_counts_opponent_wins_and_losses():
    mock_db = MagicMock()
    mock_db.players.find_one.return_value = {"_id": ObjectId(OTHER_PLAYER_ID)}
    mock_db.scores.find.return_value = [
        _make_opponent_score(True),
        _make_opponent_score(True),
        _make_opponent_score(False),
    ]
    with patch("src.modules.players.logic.get_record_logic.get_database", return_value=mock_db):
        response = client.get(f"/players/{OTHER_PLAYER_ID}/record", headers=AUTH_HEADERS)
    data = response.json()["data"]
    assert data["opponents"]["won"] == 2
    assert data["opponents"]["lost"] == 1
    assert data["team"]["won"] == 0
    assert data["team"]["lost"] == 0


def test_get_record_counts_teammate_wins_and_losses():
    mock_db = MagicMock()
    mock_db.players.find_one.return_value = {"_id": ObjectId(OTHER_PLAYER_ID)}
    mock_db.scores.find.return_value = [
        _make_teammate_score(True),
        _make_teammate_score(False),
        _make_teammate_score(False),
    ]
    with patch("src.modules.players.logic.get_record_logic.get_database", return_value=mock_db):
        response = client.get(f"/players/{OTHER_PLAYER_ID}/record", headers=AUTH_HEADERS)
    data = response.json()["data"]
    assert data["team"]["won"] == 1
    assert data["team"]["lost"] == 2
    assert data["opponents"]["won"] == 0
    assert data["opponents"]["lost"] == 0


def test_get_record_returns_404_when_player_not_found():
    mock_db = MagicMock()
    mock_db.players.find_one.return_value = None
    with patch("src.modules.players.logic.get_record_logic.get_database", return_value=mock_db):
        response = client.get(f"/players/{OTHER_PLAYER_ID}/record", headers=AUTH_HEADERS)
    assert response.status_code == 404


def test_get_record_returns_401_without_auth():
    response = client.get(f"/players/{OTHER_PLAYER_ID}/record")
    assert response.status_code in (401, 403)

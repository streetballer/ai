from unittest.mock import MagicMock, patch
from bson import ObjectId
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

COURT_ID = str(ObjectId())
PLACE_ID = str(ObjectId())
PLAYER_A1_ID = str(ObjectId())
PLAYER_A2_ID = str(ObjectId())
PLAYER_B1_ID = str(ObjectId())
PLAYER_B2_ID = str(ObjectId())

COURT_DOC = {"_id": ObjectId(COURT_ID)}
PLACE_DOC = {"_id": ObjectId(PLACE_ID)}

SCORE_DOC = {
    "_id": ObjectId(),
    "points": [5, 0],
    "players": [[PLAYER_A1_ID, PLAYER_A2_ID], [PLAYER_B1_ID, PLAYER_B2_ID]],
}

SCORE_DOC_SECOND_WIN = {
    "_id": ObjectId(),
    "points": [7, 0],
    "players": [[PLAYER_A1_ID, PLAYER_A2_ID], [PLAYER_B1_ID, PLAYER_B2_ID]],
}

SCORE_DOC_OPPONENT_WIN = {
    "_id": ObjectId(),
    "points": [0, 6],
    "players": [[PLAYER_A1_ID, PLAYER_A2_ID], [PLAYER_B1_ID, PLAYER_B2_ID]],
}


# --- GET /league (by court_id) ---

def test_get_league_by_court_returns_200():
    mock_db = MagicMock()
    mock_db.courts.get_one.return_value = COURT_DOC
    mock_db.scores.get_many.return_value = [SCORE_DOC]
    with patch("src.modules.league.logic.get_league_logic.get_database", return_value=mock_db):
        response = client.get("/league", params={"court_id": COURT_ID, "team_size": 2})
    assert response.status_code == 200
    assert "standings" in response.json()["data"]


def test_get_league_by_place_returns_200():
    mock_db = MagicMock()
    mock_db.places.get_one.return_value = PLACE_DOC
    mock_db.scores.get_many.return_value = [SCORE_DOC]
    with patch("src.modules.league.logic.get_league_logic.get_database", return_value=mock_db):
        response = client.get("/league", params={"place_id": PLACE_ID, "team_size": 2})
    assert response.status_code == 200
    assert "standings" in response.json()["data"]


def test_get_league_returns_empty_standings_when_no_scores():
    mock_db = MagicMock()
    mock_db.courts.get_one.return_value = COURT_DOC
    mock_db.scores.get_many.return_value = []
    with patch("src.modules.league.logic.get_league_logic.get_database", return_value=mock_db):
        response = client.get("/league", params={"court_id": COURT_ID, "team_size": 2})
    assert response.status_code == 200
    assert response.json()["data"]["standings"] == []


def test_get_league_returns_422_without_court_or_place():
    response = client.get("/league", params={"team_size": 2})
    assert response.status_code == 422


def test_get_league_returns_422_without_team_size():
    response = client.get("/league", params={"court_id": COURT_ID})
    assert response.status_code == 422


def test_get_league_returns_422_when_team_size_is_zero():
    response = client.get("/league", params={"court_id": COURT_ID, "team_size": 0})
    assert response.status_code == 422


def test_get_league_returns_404_when_court_not_found():
    mock_db = MagicMock()
    mock_db.courts.get_one.return_value = None
    with patch("src.modules.league.logic.get_league_logic.get_database", return_value=mock_db):
        response = client.get("/league", params={"court_id": COURT_ID, "team_size": 2})
    assert response.status_code == 404


def test_get_league_returns_404_when_place_not_found():
    mock_db = MagicMock()
    mock_db.places.get_one.return_value = None
    with patch("src.modules.league.logic.get_league_logic.get_database", return_value=mock_db):
        response = client.get("/league", params={"place_id": PLACE_ID, "team_size": 2})
    assert response.status_code == 404


def test_get_league_standings_sorted_by_points_descending():
    mock_db = MagicMock()
    mock_db.courts.get_one.return_value = COURT_DOC
    mock_db.scores.get_many.return_value = [SCORE_DOC, SCORE_DOC_OPPONENT_WIN]
    with patch("src.modules.league.logic.get_league_logic.get_database", return_value=mock_db):
        response = client.get("/league", params={"court_id": COURT_ID, "team_size": 2})
    assert response.status_code == 200
    standings = response.json()["data"]["standings"]
    assert len(standings) == 2
    assert standings[0]["points"] >= standings[1]["points"]


def test_get_league_aggregates_points_across_multiple_scores():
    mock_db = MagicMock()
    mock_db.courts.get_one.return_value = COURT_DOC
    mock_db.scores.get_many.return_value = [SCORE_DOC, SCORE_DOC_SECOND_WIN]
    with patch("src.modules.league.logic.get_league_logic.get_database", return_value=mock_db):
        response = client.get("/league", params={"court_id": COURT_ID, "team_size": 2})
    assert response.status_code == 200
    standings = response.json()["data"]["standings"]
    winner_entry = next(e for e in standings if set(e["players"]) == {PLAYER_A1_ID, PLAYER_A2_ID})
    assert winner_entry["points"] == 12


def test_get_league_queries_scores_with_confirmed_and_expr_filter():
    mock_db = MagicMock()
    mock_db.courts.get_one.return_value = COURT_DOC
    mock_db.scores.get_many.return_value = []
    with patch("src.modules.league.logic.get_league_logic.get_database", return_value=mock_db):
        client.get("/league", params={"court_id": COURT_ID, "team_size": 3})
    call_args = mock_db.scores.get_many.call_args
    query = call_args[0][0]
    assert query.get("confirmed") is True
    assert query.get("court_id") == COURT_ID
    assert "$expr" in query


def test_get_league_uses_place_ids_filter_when_place_id_given():
    mock_db = MagicMock()
    mock_db.places.get_one.return_value = PLACE_DOC
    mock_db.scores.get_many.return_value = []
    with patch("src.modules.league.logic.get_league_logic.get_database", return_value=mock_db):
        client.get("/league", params={"place_id": PLACE_ID, "team_size": 2})
    call_args = mock_db.scores.get_many.call_args
    query = call_args[0][0]
    assert query.get("place_ids") == PLACE_ID

from unittest.mock import MagicMock, patch, call
from datetime import datetime, timezone, timedelta
from bson import ObjectId
from fastapi.testclient import TestClient
from src.main import app
from src.common.libraries.jwt import create_access_token

client = TestClient(app)

PLAYER_ID = str(ObjectId())
OTHER_PLAYER_ID = str(ObjectId())
TEAM_A_ID = str(ObjectId())
TEAM_B_ID = str(ObjectId())
COURT_ID = str(ObjectId())
SCORE_ID = str(ObjectId())
AUTH_HEADERS = {"Authorization": f"Bearer {create_access_token(PLAYER_ID)}"}

NOW = datetime.now(timezone.utc)
ACTIVE_LAST_ACTIVITY = NOW - timedelta(hours=1)

PLAYER_DOC = {
    "_id": ObjectId(PLAYER_ID),
    "team_id": TEAM_A_ID,
    "rating": 5,
}

OPPONENT_DOC = {
    "_id": ObjectId(OTHER_PLAYER_ID),
    "team_id": TEAM_B_ID,
    "rating": 5,
}

TEAM_A_DOC = {
    "_id": ObjectId(TEAM_A_ID),
    "color": "#FF0000",
    "geolocation": {"type": "Point", "coordinates": [-118.25, 34.05]},
    "court_id": COURT_ID,
    "last_activity": ACTIVE_LAST_ACTIVITY,
}

TEAM_B_DOC = {
    "_id": ObjectId(TEAM_B_ID),
    "color": "#0000FF",
    "geolocation": {"type": "Point", "coordinates": [-118.25, 34.05]},
    "court_id": COURT_ID,
    "last_activity": ACTIVE_LAST_ACTIVITY,
}

COURT_DOC = {
    "_id": ObjectId(COURT_ID),
    "place_ids": [],
}

SCORE_DOC = {
    "_id": ObjectId(SCORE_ID),
    "timestamp": NOW,
    "result": [10, 5],
    "points": [5, 0],
    "players": [[PLAYER_ID], [OTHER_PLAYER_ID]],
    "teams": [TEAM_A_ID, TEAM_B_ID],
    "colors": ["#FF0000", "#0000FF"],
    "confirmations": [PLAYER_ID],
    "rejections": [],
    "confirmed": False,
    "player_ids": [PLAYER_ID, OTHER_PLAYER_ID],
    "geolocation": {"type": "Point", "coordinates": [-118.25, 34.05]},
    "court_id": COURT_ID,
    "place_ids": [],
}

PUBLIC_PLAYER_DOC = {
    "_id": ObjectId(PLAYER_ID),
    "username": "streetballer",
    "language": "en",
    "team_id": TEAM_A_ID,
}


# --- GET /scores ---

def test_get_scores_returns_200():
    mock_db = MagicMock()
    mock_db.scores.get_many.return_value = [SCORE_DOC]
    with patch("src.modules.scores.logic.get_scores_logic.get_database", return_value=mock_db):
        response = client.get("/scores", params={"player_id": PLAYER_ID}, headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert "scores" in response.json()["data"]


def test_get_scores_returns_empty_list_when_no_scores():
    mock_db = MagicMock()
    mock_db.scores.get_many.return_value = []
    with patch("src.modules.scores.logic.get_scores_logic.get_database", return_value=mock_db):
        response = client.get("/scores", params={"player_id": PLAYER_ID}, headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert response.json()["data"]["scores"] == []


def test_get_scores_filters_by_confirmed():
    mock_db = MagicMock()
    mock_db.scores.get_many.return_value = []
    with patch("src.modules.scores.logic.get_scores_logic.get_database", return_value=mock_db):
        response = client.get("/scores", params={"player_id": PLAYER_ID, "confirmed": True}, headers=AUTH_HEADERS)
    assert response.status_code == 200
    call_args = mock_db.scores.get_many.call_args
    assert call_args[0][0].get("confirmed") is True


def test_get_scores_returns_401_without_auth():
    response = client.get("/scores", params={"player_id": PLAYER_ID})
    assert response.status_code in (401, 403)


def test_get_scores_returns_422_without_player_id():
    response = client.get("/scores", headers=AUTH_HEADERS)
    assert response.status_code == 422


# --- POST /scores ---

def test_submit_score_returns_200():
    mock_db = MagicMock()
    mock_db.players.get_many.side_effect = [
        [PLAYER_DOC, OPPONENT_DOC],
        [PLAYER_DOC, OPPONENT_DOC],
    ]
    mock_db.teams.get_one.side_effect = [TEAM_A_DOC, TEAM_B_DOC]
    mock_db.courts.get_one.return_value = COURT_DOC
    mock_db.scores.insert_one.return_value = SCORE_ID
    with patch("src.modules.scores.logic.submit_score_logic.get_database", return_value=mock_db):
        response = client.post(
            "/scores",
            json={"score_1": 10, "score_2": 5, "opponent_id": OTHER_PLAYER_ID},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 200
    assert "score" in response.json()["data"]


def test_submit_score_returns_401_without_auth():
    response = client.post("/scores", json={"score_1": 10, "score_2": 5, "opponent_id": OTHER_PLAYER_ID})
    assert response.status_code in (401, 403)


def test_submit_score_returns_422_when_tied():
    response = client.post(
        "/scores",
        json={"score_1": 7, "score_2": 7, "opponent_id": OTHER_PLAYER_ID},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 422


def test_submit_score_returns_422_when_score_out_of_range():
    response = client.post(
        "/scores",
        json={"score_1": 100, "score_2": 5, "opponent_id": OTHER_PLAYER_ID},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 422


def test_submit_score_returns_422_when_player_has_no_active_team():
    mock_db = MagicMock()
    mock_db.players.get_many.return_value = [{**PLAYER_DOC, "team_id": ""}]
    mock_db.teams.get_one.return_value = None
    with patch("src.modules.scores.logic.submit_score_logic.get_database", return_value=mock_db):
        response = client.post(
            "/scores",
            json={"score_1": 10, "score_2": 5, "opponent_id": OTHER_PLAYER_ID},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 422


def test_submit_score_returns_422_when_opponent_not_found():
    mock_db = MagicMock()
    mock_db.players.get_many.return_value = [PLAYER_DOC]
    mock_db.teams.get_one.return_value = TEAM_A_DOC
    with patch("src.modules.scores.logic.submit_score_logic.get_database", return_value=mock_db):
        response = client.post(
            "/scores",
            json={"score_1": 10, "score_2": 5, "opponent_id": OTHER_PLAYER_ID},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 422


def test_submit_score_returns_422_when_opponent_has_no_active_team():
    mock_db = MagicMock()
    mock_db.players.get_many.return_value = [PLAYER_DOC, {**OPPONENT_DOC, "team_id": ""}]
    mock_db.teams.get_one.side_effect = [TEAM_A_DOC, None]
    with patch("src.modules.scores.logic.submit_score_logic.get_database", return_value=mock_db):
        response = client.post(
            "/scores",
            json={"score_1": 10, "score_2": 5, "opponent_id": OTHER_PLAYER_ID},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 422


def test_submit_score_returns_422_when_same_team():
    mock_db = MagicMock()
    mock_db.players.get_many.return_value = [
        {**PLAYER_DOC, "team_id": TEAM_A_ID},
        {**OPPONENT_DOC, "team_id": TEAM_A_ID},
    ]
    mock_db.teams.get_one.side_effect = [TEAM_A_DOC, TEAM_A_DOC]
    with patch("src.modules.scores.logic.submit_score_logic.get_database", return_value=mock_db):
        response = client.post(
            "/scores",
            json={"score_1": 10, "score_2": 5, "opponent_id": OTHER_PLAYER_ID},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 422


def test_submit_score_updates_ratings_when_winner_avg_leq_loser_avg():
    mock_db = MagicMock()
    weaker_player = {**PLAYER_DOC, "rating": 3}
    stronger_opponent = {**OPPONENT_DOC, "rating": 7}
    mock_db.players.get_many.side_effect = [
        [weaker_player, stronger_opponent],
        [weaker_player, stronger_opponent],
    ]
    mock_db.teams.get_one.side_effect = [TEAM_A_DOC, TEAM_B_DOC]
    mock_db.courts.get_one.return_value = COURT_DOC
    mock_db.scores.insert_one.return_value = SCORE_ID
    with patch("src.modules.scores.logic.submit_score_logic.get_database", return_value=mock_db):
        response = client.post(
            "/scores",
            json={"score_1": 10, "score_2": 5, "opponent_id": OTHER_PLAYER_ID},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 200
    assert mock_db.players.update_many.call_count == 2


def test_submit_score_skips_rating_update_when_winner_has_higher_avg():
    mock_db = MagicMock()
    stronger_player = {**PLAYER_DOC, "rating": 7}
    weaker_opponent = {**OPPONENT_DOC, "rating": 3}
    mock_db.players.get_many.side_effect = [
        [stronger_player, weaker_opponent],
        [stronger_player, weaker_opponent],
    ]
    mock_db.teams.get_one.side_effect = [TEAM_A_DOC, TEAM_B_DOC]
    mock_db.courts.get_one.return_value = COURT_DOC
    mock_db.scores.insert_one.return_value = SCORE_ID
    with patch("src.modules.scores.logic.submit_score_logic.get_database", return_value=mock_db):
        response = client.post(
            "/scores",
            json={"score_1": 10, "score_2": 5, "opponent_id": OTHER_PLAYER_ID},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 200
    mock_db.players.update_many.assert_not_called()


# --- GET /scores/:score_id ---

def test_get_score_returns_200():
    mock_db = MagicMock()
    mock_db.scores.get_one.return_value = SCORE_DOC
    mock_db.players.get_many.return_value = [PUBLIC_PLAYER_DOC]
    with patch("src.modules.scores.logic.get_score_logic.get_database", return_value=mock_db):
        response = client.get(f"/scores/{SCORE_ID}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "score" in data
    assert "players" in data


def test_get_score_returns_404_when_not_found():
    mock_db = MagicMock()
    mock_db.scores.get_one.return_value = None
    with patch("src.modules.scores.logic.get_score_logic.get_database", return_value=mock_db):
        response = client.get(f"/scores/{SCORE_ID}")
    assert response.status_code == 404


# --- POST /scores/:score_id/confirm ---

def test_confirm_score_returns_200():
    mock_db = MagicMock()
    mock_db.scores.get_one.return_value = {
        **SCORE_DOC,
        "confirmations": [],
        "player_ids": [PLAYER_ID, OTHER_PLAYER_ID],
    }
    with patch("src.modules.scores.logic.confirm_score_logic.get_database", return_value=mock_db):
        response = client.post(f"/scores/{SCORE_ID}/confirm", headers=AUTH_HEADERS)
    assert response.status_code == 200
    mock_db.scores.update_one.assert_called()


def test_confirm_score_returns_401_without_auth():
    response = client.post(f"/scores/{SCORE_ID}/confirm")
    assert response.status_code in (401, 403)


def test_confirm_score_returns_403_when_not_in_score():
    mock_db = MagicMock()
    mock_db.scores.get_one.return_value = {
        **SCORE_DOC,
        "player_ids": [OTHER_PLAYER_ID],
    }
    with patch("src.modules.scores.logic.confirm_score_logic.get_database", return_value=mock_db):
        response = client.post(f"/scores/{SCORE_ID}/confirm", headers=AUTH_HEADERS)
    assert response.status_code == 403


def test_confirm_score_returns_404_when_not_found():
    mock_db = MagicMock()
    mock_db.scores.get_one.return_value = None
    with patch("src.modules.scores.logic.confirm_score_logic.get_database", return_value=mock_db):
        response = client.post(f"/scores/{SCORE_ID}/confirm", headers=AUTH_HEADERS)
    assert response.status_code == 404


def test_confirm_score_sets_confirmed_when_both_sides_confirmed():
    mock_db = MagicMock()
    mock_db.scores.get_one.return_value = {
        **SCORE_DOC,
        "players": [[PLAYER_ID], [OTHER_PLAYER_ID]],
        "confirmations": [OTHER_PLAYER_ID],
        "player_ids": [PLAYER_ID, OTHER_PLAYER_ID],
        "confirmed": False,
    }
    with patch("src.modules.scores.logic.confirm_score_logic.get_database", return_value=mock_db):
        response = client.post(f"/scores/{SCORE_ID}/confirm", headers=AUTH_HEADERS)
    assert response.status_code == 200
    set_call = mock_db.scores.update_one.call_args_list[-1]
    assert set_call[0][1] == {"$set": {"confirmed": True}}


# --- POST /scores/:score_id/reject ---

def test_reject_score_returns_200():
    mock_db = MagicMock()
    mock_db.scores.get_one.return_value = {
        **SCORE_DOC,
        "rejections": [],
        "confirmations": [],
        "players": [[PLAYER_ID], [OTHER_PLAYER_ID]],
        "player_ids": [PLAYER_ID, OTHER_PLAYER_ID],
    }
    with patch("src.modules.scores.logic.reject_score_logic.get_database", return_value=mock_db):
        response = client.post(f"/scores/{SCORE_ID}/reject", headers=AUTH_HEADERS)
    assert response.status_code == 200
    mock_db.scores.update_one.assert_called()


def test_reject_score_returns_401_without_auth():
    response = client.post(f"/scores/{SCORE_ID}/reject")
    assert response.status_code in (401, 403)


def test_reject_score_returns_403_when_not_in_score():
    mock_db = MagicMock()
    mock_db.scores.get_one.return_value = {
        **SCORE_DOC,
        "player_ids": [OTHER_PLAYER_ID],
    }
    with patch("src.modules.scores.logic.reject_score_logic.get_database", return_value=mock_db):
        response = client.post(f"/scores/{SCORE_ID}/reject", headers=AUTH_HEADERS)
    assert response.status_code == 403


def test_reject_score_returns_404_when_not_found():
    mock_db = MagicMock()
    mock_db.scores.get_one.return_value = None
    with patch("src.modules.scores.logic.reject_score_logic.get_database", return_value=mock_db):
        response = client.post(f"/scores/{SCORE_ID}/reject", headers=AUTH_HEADERS)
    assert response.status_code == 404


def test_reject_score_deletes_when_majority_of_side_rejects():
    mock_db = MagicMock()
    mock_db.scores.get_one.return_value = {
        **SCORE_DOC,
        "players": [[PLAYER_ID], [OTHER_PLAYER_ID]],
        "rejections": [],
        "confirmations": [],
        "player_ids": [PLAYER_ID, OTHER_PLAYER_ID],
    }
    with patch("src.modules.scores.logic.reject_score_logic.get_database", return_value=mock_db):
        response = client.post(f"/scores/{SCORE_ID}/reject", headers=AUTH_HEADERS)
    assert response.status_code == 200
    mock_db.scores.delete_one.assert_called_once()

from unittest.mock import MagicMock, patch
from bson import ObjectId
from fastapi.testclient import TestClient
from src.main import app
from src.common.libraries.jwt import create_access_token

client = TestClient(app)

PLAYER_ID = str(ObjectId())
AUTH_HEADERS = {"Authorization": f"Bearer {create_access_token(PLAYER_ID)}"}
COURT_ID = str(ObjectId())
PLACE_ID = str(ObjectId())
PARENT_PLACE_ID = str(ObjectId())

COURT_DOC = {
    "_id": ObjectId(COURT_ID),
    "name": "Venice Beach Court",
    "geolocation": {"type": "Point", "coordinates": [-118.47, 33.98]},
    "place_ids": [],
}

PLACE_DOC = {
    "_id": ObjectId(PLACE_ID),
    "address": ["Venice", "Los Angeles", "US"],
    "is_parent": False,
    "parent_ids": [PARENT_PLACE_ID],
    "geolocation": {"type": "Point", "coordinates": [-118.47, 33.98]},
}


# --- GET /courts ---

def test_search_courts_returns_200():
    mock_db = MagicMock()
    mock_db.courts.get_many.return_value = [COURT_DOC]
    with patch("src.modules.courts.logic.search_courts_logic.get_database", return_value=mock_db):
        response = client.get("/courts", params={"lon": -118.47, "lat": 33.98})
    assert response.status_code == 200
    assert "courts" in response.json()["data"]


def test_search_courts_accepts_custom_radius():
    mock_db = MagicMock()
    mock_db.courts.get_many.return_value = [COURT_DOC]
    with patch("src.modules.courts.logic.search_courts_logic.get_database", return_value=mock_db):
        response = client.get("/courts", params={"lon": -118.47, "lat": 33.98, "radius": 500})
    assert response.status_code == 200


def test_search_courts_returns_422_without_params():
    response = client.get("/courts")
    assert response.status_code == 422


def test_search_courts_returns_422_with_only_lon():
    response = client.get("/courts", params={"lon": -118.47})
    assert response.status_code == 422


# --- POST /courts ---

def test_add_court_returns_200():
    mock_db = MagicMock()
    mock_db.courts.get_one.side_effect = [None, COURT_DOC]
    mock_db.courts.insert_one.return_value = COURT_ID
    mock_db.places.get_one.return_value = None
    with patch("src.modules.courts.logic.add_court_logic.get_database", return_value=mock_db):
        response = client.post(
            "/courts",
            json={"lon": -118.47, "lat": 33.98, "name": "Venice Beach Court"},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 200
    assert "court" in response.json()["data"]


def test_add_court_assigns_place_ids():
    mock_db = MagicMock()
    court_with_places = {**COURT_DOC, "place_ids": [PLACE_ID, PARENT_PLACE_ID]}
    mock_db.courts.get_one.side_effect = [None, court_with_places]
    mock_db.courts.insert_one.return_value = COURT_ID
    mock_db.places.get_one.return_value = PLACE_DOC
    with patch("src.modules.courts.logic.add_court_logic.get_database", return_value=mock_db):
        response = client.post(
            "/courts",
            json={"lon": -118.47, "lat": 33.98, "name": "Venice Beach Court"},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 200
    court = response.json()["data"]["court"]
    assert PLACE_ID in court["place_ids"]
    assert PARENT_PLACE_ID in court["place_ids"]


def test_add_court_returns_409_when_duplicate():
    mock_db = MagicMock()
    mock_db.courts.get_one.return_value = COURT_DOC
    with patch("src.modules.courts.logic.add_court_logic.get_database", return_value=mock_db):
        response = client.post(
            "/courts",
            json={"lon": -118.47, "lat": 33.98, "name": "Duplicate Court"},
            headers=AUTH_HEADERS,
        )
    assert response.status_code == 409


def test_add_court_returns_401_without_auth():
    response = client.post("/courts", json={"lon": -118.47, "lat": 33.98, "name": "Court"})
    assert response.status_code in (401, 403)


def test_add_court_returns_422_with_missing_fields():
    response = client.post("/courts", json={"lon": -118.47}, headers=AUTH_HEADERS)
    assert response.status_code == 422


# --- GET /courts/:court_id ---

def test_get_court_returns_200():
    mock_db = MagicMock()
    mock_db.courts.get_one.return_value = COURT_DOC
    with patch("src.modules.courts.logic.get_court_logic.get_database", return_value=mock_db):
        response = client.get(f"/courts/{COURT_ID}")
    assert response.status_code == 200
    assert "court" in response.json()["data"]
    assert response.json()["data"]["court"]["name"] == "Venice Beach Court"


def test_get_court_returns_404_when_not_found():
    mock_db = MagicMock()
    mock_db.courts.get_one.return_value = None
    with patch("src.modules.courts.logic.get_court_logic.get_database", return_value=mock_db):
        response = client.get(f"/courts/{COURT_ID}")
    assert response.status_code == 404

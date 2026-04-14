from unittest.mock import MagicMock, patch
from bson import ObjectId
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

PLACE_DOC = {
    "_id": ObjectId(),
    "name": "Los Angeles",
    "type": "place",
    "geolocation": {"type": "Point", "coordinates": [-118.25, 34.05]},
    "geolocation_box": None,
    "parent_ids": [],
}


def test_search_places_by_text_returns_200():
    mock_db = MagicMock()
    mock_db.places.get_many.return_value = [PLACE_DOC]
    with patch("src.modules.places.logic.search_places_logic.get_database", return_value=mock_db):
        response = client.get("/places", params={"text": "Los Angeles"})
    assert response.status_code == 200
    assert "places" in response.json()["data"]


def test_search_places_by_location_returns_200():
    mock_db = MagicMock()
    mock_db.places.get_many.return_value = [PLACE_DOC]
    with patch("src.modules.places.logic.search_places_logic.get_database", return_value=mock_db):
        response = client.get("/places", params={"lon": -118.25, "lat": 34.05})
    assert response.status_code == 200


def test_search_places_by_text_and_location_returns_200():
    mock_db = MagicMock()
    mock_db.places.get_many.return_value = [PLACE_DOC]
    with patch("src.modules.places.logic.search_places_logic.get_database", return_value=mock_db):
        response = client.get("/places", params={"text": "Los Angeles", "lon": -118.25, "lat": 34.05})
    assert response.status_code == 200


def test_search_places_returns_422_with_no_params():
    response = client.get("/places")
    assert response.status_code == 422


def test_search_places_returns_422_with_only_lon():
    response = client.get("/places", params={"lon": -118.25})
    assert response.status_code == 422

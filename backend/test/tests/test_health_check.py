from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_check_returns_200():
    response = client.get("/health-check")
    assert response.status_code == 200


def test_health_check_returns_response_format():
    response = client.get("/health-check")
    body = response.json()
    assert "message" in body
    assert "data" in body
    assert isinstance(body["message"], str)
    assert isinstance(body["data"], dict)

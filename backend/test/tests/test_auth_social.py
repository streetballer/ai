from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_google_auth_returns_501():
    response = client.post("/auth/google", json={"token": "any-token"})
    assert response.status_code == 501


def test_apple_auth_returns_501():
    response = client.post("/auth/apple", json={"token": "any-token"})
    assert response.status_code == 501


def test_facebook_auth_returns_501():
    response = client.post("/auth/facebook", json={"token": "any-token"})
    assert response.status_code == 501


def test_google_auth_returns_422_when_token_missing():
    response = client.post("/auth/google", json={})
    assert response.status_code == 422


def test_apple_auth_returns_422_when_token_missing():
    response = client.post("/auth/apple", json={})
    assert response.status_code == 422


def test_facebook_auth_returns_422_when_token_missing():
    response = client.post("/auth/facebook", json={})
    assert response.status_code == 422

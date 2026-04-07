from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch
import jwt
from bson import ObjectId
from fastapi.testclient import TestClient
from src.main import app
from src.common.environment.config import JWT_SECRET

client = TestClient(app)

PLAYER_ID = str(ObjectId())


def make_token(player_id: str, token_type: str, expired: bool = False) -> str:
    exp = datetime.now(timezone.utc) + timedelta(seconds=-1 if expired else 86400)
    return jwt.encode({"sub": player_id, "type": token_type, "exp": exp}, JWT_SECRET, algorithm="HS256")


def test_verification_returns_200_with_valid_token():
    token = make_token(PLAYER_ID, "email_verification")
    mock_db = MagicMock()
    with patch("src.modules.auth.logic.verification_logic.get_database", return_value=mock_db):
        response = client.post(f"/auth/verification/{token}")
    assert response.status_code == 200


def test_verification_sets_email_verified_true():
    token = make_token(PLAYER_ID, "email_verification")
    mock_db = MagicMock()
    with patch("src.modules.auth.logic.verification_logic.get_database", return_value=mock_db):
        client.post(f"/auth/verification/{token}")
    call_args = mock_db.players.update_one.call_args
    assert call_args[0][1]["$set"]["email_verified"] is True


def test_verification_returns_498_for_expired_token():
    token = make_token(PLAYER_ID, "email_verification", expired=True)
    response = client.post(f"/auth/verification/{token}")
    assert response.status_code == 498


def test_verification_returns_498_for_wrong_token_type():
    token = make_token(PLAYER_ID, "password_reset")
    response = client.post(f"/auth/verification/{token}")
    assert response.status_code == 498


def test_verification_returns_498_for_invalid_token():
    response = client.post("/auth/verification/not-a-valid-token")
    assert response.status_code == 498

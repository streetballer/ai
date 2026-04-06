from src.common.environment.config import FRONTEND_URL
from src.common.libraries.database import get_database
from src.common.libraries.email import send_email
from src.common.libraries.hash import hash_value
from src.common.libraries.jwt import create_password_reset_token
from src.common.utilities.localize import localize


def request_password_reset(username: str | None, email: str | None) -> None:
    db = get_database()
    query = {"username": username} if username else {"email": email}
    player = db.players.get_one(query, {"_id": 1, "email": 1, "username": 1})
    if player is None:
        return
    token = create_password_reset_token(player["_id"])
    link = f"{FRONTEND_URL}/auth/reset?token={token}"
    subject = localize("password_reset_subject")
    body = localize("password_reset_body", username=player["username"], link=link)
    send_email(player["email"], subject, body)


def reset_password(player_id: str, new_password: str) -> None:
    db = get_database()
    db.players.update_one(
        {"_id": player_id},
        {"$set": {"password_hash": hash_value(new_password), "refresh_token_hash": ""}},
    )

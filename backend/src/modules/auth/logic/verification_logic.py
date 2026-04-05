from src.common.environment.config import FRONTEND_URL
from src.common.libraries.database import get_database
from src.common.libraries.email import send_email
from src.common.libraries.jwt import create_verification_token
from src.common.utilities.localize import localize


def send_verification_email(player_id: str, email: str, username: str) -> None:
    token = create_verification_token(player_id)
    link = f"{FRONTEND_URL}/auth/verification/{token}"
    subject = localize("email_verification_subject")
    body = localize("email_verification_body", username=username, link=link)
    send_email(email, subject, body)


def verify_email(player_id: str) -> None:
    db = get_database()
    db.players.update_one(
        {"_id": player_id},
        {"$set": {"email_verified": True}},
    )

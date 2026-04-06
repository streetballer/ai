from datetime import datetime, timezone
from bson import ObjectId
from src.common.libraries.database import get_database, DuplicateEntryError
from src.common.libraries.hash import hash_value
from src.common.libraries.jwt import create_access_token, create_refresh_token
from src.common.models.player import Player
from src.modules.auth.models.auth_tokens import AuthTokens


def create_player(username: str, email: str, password: str) -> tuple[str | None, AuthTokens | None]:
    player_id = str(ObjectId())
    access_token = create_access_token(player_id)
    refresh_token = create_refresh_token(player_id)
    player = Player(
        id=player_id,
        email=email,
        username=username,
        password_hash=hash_value(password),
        refresh_token_hash=hash_value(refresh_token),
        created=datetime.now(timezone.utc),
    )
    db = get_database()
    try:
        db.players.insert_one(player.to_doc())
    except DuplicateEntryError as exc:
        if exc.key == "username":
            return "username_taken", None
        return "email_taken", None
    return None, AuthTokens(player_id=player_id, access_token=access_token, refresh_token=refresh_token)

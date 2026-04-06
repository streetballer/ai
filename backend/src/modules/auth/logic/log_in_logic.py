from src.common.libraries.database import get_database
from src.common.libraries.hash import hash_value, verify_hash
from src.common.libraries.jwt import create_access_token, create_refresh_token
from src.common.models.player import Player
from src.modules.auth.models.auth_tokens import AuthTokens

PLAYER_AUTH_PROJECTION = {"_id": 1, "password_hash": 1, "refresh_token_hash": 1}


def authenticate_player(password: str, username: str | None, email: str | None) -> AuthTokens | None:
    db = get_database()
    query = {"username": username} if username else {"email": email}
    doc = db.players.find_one(query, PLAYER_AUTH_PROJECTION)
    if doc is None:
        return None
    player = Player.from_doc(doc)
    if not verify_hash(password, player.password_hash):
        return None
    access_token = create_access_token(player.id)
    refresh_token = create_refresh_token(player.id)
    db.players.update_one(
        {"_id": doc["_id"]},
        {"$set": {"refresh_token_hash": hash_value(refresh_token)}},
    )
    return AuthTokens(access_token=access_token, refresh_token=refresh_token)

from src.common.libraries.database import get_database
from src.common.libraries.hash import hash_value, verify_hash
from src.common.libraries.jwt import create_access_token, create_refresh_token
from src.common.models.player import Player
from src.modules.auth.models.auth_tokens import AuthTokens

PLAYER_TOKEN_PROJECTION = {"_id": 1, "refresh_token_hash": 1}


def rotate_tokens(player_id: str, refresh_token: str) -> AuthTokens | None:
    db = get_database()
    doc = db.players.find_one({"_id": player_id}, PLAYER_TOKEN_PROJECTION)
    if doc is None:
        return None
    player = Player.from_doc(doc)
    if not verify_hash(refresh_token, player.refresh_token_hash):
        return None
    access_token = create_access_token(player_id)
    new_refresh_token = create_refresh_token(player_id)
    db.players.update_one(
        {"_id": player_id},
        {"$set": {"refresh_token_hash": hash_value(new_refresh_token)}},
    )
    return AuthTokens(access_token=access_token, refresh_token=new_refresh_token)

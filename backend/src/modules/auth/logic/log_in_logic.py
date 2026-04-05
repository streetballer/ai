from src.common.libraries.database import get_database
from src.common.libraries.hash import hash_value, verify_hash
from src.common.libraries.jwt import create_access_token, create_refresh_token


def authenticate_player(password: str, username: str | None, email: str | None) -> dict | None:
    db = get_database()
    query = {"username": username} if username else {"email": email}
    player = db.players.find_one(query)
    if player is None:
        return None
    if not verify_hash(password, player.get("password_hash", "")):
        return None
    player_id = player["_id"]
    access_token = create_access_token(player_id)
    refresh_token = create_refresh_token(player_id)
    db.players.update_one(
        {"_id": player_id},
        {"$set": {"refresh_token_hash": hash_value(refresh_token)}},
    )
    return {"access_token": access_token, "refresh_token": refresh_token}

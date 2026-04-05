from src.common.libraries.database import get_database
from src.common.libraries.hash import hash_value, verify_hash
from src.common.libraries.jwt import create_access_token, create_refresh_token


def rotate_tokens(player_id: str, refresh_token: str) -> dict | None:
    db = get_database()
    player = db.players.find_one({"_id": player_id})
    if player is None:
        return None
    if not verify_hash(refresh_token, player.get("refresh_token_hash", "")):
        return None
    access_token = create_access_token(player_id)
    new_refresh_token = create_refresh_token(player_id)
    db.players.update_one(
        {"_id": player_id},
        {"$set": {"refresh_token_hash": hash_value(new_refresh_token)}},
    )
    return {"access_token": access_token, "refresh_token": new_refresh_token}

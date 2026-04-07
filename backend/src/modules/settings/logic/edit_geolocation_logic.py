from datetime import datetime, timezone
from bson import ObjectId
from src.common.libraries.database import get_database


def edit_geolocation(player_id: str, lon: float, lat: float) -> None:
    db = get_database()
    geolocation = {"type": "Point", "coordinates": [lon, lat]}
    db.players.update_one(
        {"_id": ObjectId(player_id)},
        {"$set": {"geolocation": geolocation, "geolocation_timestamp": datetime.now(timezone.utc)}},
    )

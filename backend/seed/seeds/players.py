from datetime import datetime, timezone
from bson import ObjectId
from src.common.libraries.database import Database
from src.common.libraries.hash import hash_value
from src.common.models.player import Player
from seed.data.reference import LAT, LON
from seed.helpers.geo import point

_PASSWORD_HASH = hash_value("streetballer123")

_PLAYERS = [
    ("carlos_g", "carlos@streetballer.com", 6),
    ("pedro_m", "pedro@streetballer.com", 5),
    ("juan_r", "juan@streetballer.com", 5),
    ("miguel_a", "miguel@streetballer.com", 6),
    ("ana_l", "ana@streetballer.com", 7),
    ("david_f", "david@streetballer.com", 5),
    ("lucia_v", "lucia@streetballer.com", 6),
    ("marcos_s", "marcos@streetballer.com", 5),
]


def seed_players(db: Database) -> list[str]:
    now = datetime.now(timezone.utc)
    player_ids = [str(ObjectId()) for _ in _PLAYERS]
    docs = []
    for i, (player_id, (username, email, rating)) in enumerate(zip(player_ids, _PLAYERS)):
        lat_offset = (i - 4) * 0.002
        lon_offset = (i % 3 - 1) * 0.003
        player = Player(
            id=player_id,
            email=email,
            email_verified=True,
            username=username,
            password_hash=_PASSWORD_HASH,
            language="en",
            rating=rating,
            geolocation=point(LON + lon_offset, LAT + lat_offset),
            geolocation_timestamp=now,
            created=now,
        )
        docs.append(player.to_doc())
    db.players.insert_many(docs)
    return player_ids

from src.common.libraries.database import Database
from seed.data.reference import LAT, LON
from seed.helpers.geo import point


def seed_places(db: Database) -> list[str]:
    granada_id = db.places.insert_one({
        "geolocation": point(LON - 0.003, LAT + 0.003),
        "geolocation_box": [-3.640, 37.155, -3.560, 37.200],
        "address": ["Granada", "Andalucía", "Spain"],
        "is_parent": True,
        "parent_ids": [],
    })

    centro_id = db.places.insert_one({
        "geolocation": point(LON + 0.003, LAT + 0.003),
        "geolocation_box": [-3.610, 37.170, -3.585, 37.185],
        "address": ["Centro", "Granada", "Andalucía", "Spain"],
        "is_parent": False,
        "parent_ids": [granada_id],
    })

    realejo_id = db.places.insert_one({
        "geolocation": point(LON, LAT),
        "geolocation_box": [-3.608, 37.168, -3.590, 37.180],
        "address": ["Realejo", "Granada", "Andalucía", "Spain"],
        "is_parent": False,
        "parent_ids": [granada_id],
    })

    albaicin_id = db.places.insert_one({
        "geolocation": point(LON + 0.009, LAT + 0.007),
        "geolocation_box": [-3.600, 37.175, -3.580, 37.188],
        "address": ["Albaicín", "Granada", "Andalucía", "Spain"],
        "is_parent": False,
        "parent_ids": [granada_id],
    })

    zaidin_id = db.places.insert_one({
        "geolocation": point(LON - 0.006, LAT - 0.016),
        "geolocation_box": [-3.620, 37.148, -3.590, 37.168],
        "address": ["Zaidín", "Granada", "Andalucía", "Spain"],
        "is_parent": False,
        "parent_ids": [granada_id],
    })

    return [granada_id, centro_id, realejo_id, albaicin_id, zaidin_id]

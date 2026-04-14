from src.common.libraries.database import Database
from seed.data.reference import LAT, LON
from seed.helpers.geo import point


def seed_places(db: Database) -> list[str]:
    spain_id = db.places.insert_one({
        "name": "Spain",
        "type": "country",
        "geolocation": point(-3.7038, 40.4168),
        "geolocation_box": [-18.1674, 27.6377, 4.3276, 43.7913],
        "parent_ids": [],
    })

    andalucia_id = db.places.insert_one({
        "name": "Andalucía",
        "type": "state",
        "geolocation": point(-4.7278, 37.5443),
        "geolocation_box": [-7.5225, 36.0001, -1.6305, 38.7291],
        "parent_ids": [spain_id],
    })

    granada_id = db.places.insert_one({
        "name": "Granada",
        "type": "province",
        "geolocation": point(LON - 0.003, LAT + 0.003),
        "geolocation_box": [-3.640, 37.155, -3.560, 37.200],
        "parent_ids": [andalucia_id, spain_id],
    })

    neighbourhood_ids = db.places.insert_many([
        {
            "name": "Centro",
            "type": "place",
            "geolocation": point(LON + 0.003, LAT + 0.003),
            "geolocation_box": [-3.610, 37.170, -3.585, 37.185],
            "parent_ids": [granada_id, andalucia_id, spain_id],
        },
        {
            "name": "Realejo",
            "type": "place",
            "geolocation": point(LON, LAT),
            "geolocation_box": [-3.608, 37.168, -3.590, 37.180],
            "parent_ids": [granada_id, andalucia_id, spain_id],
        },
        {
            "name": "Albaicín",
            "type": "place",
            "geolocation": point(LON + 0.009, LAT + 0.007),
            "geolocation_box": [-3.600, 37.175, -3.580, 37.188],
            "parent_ids": [granada_id, andalucia_id, spain_id],
        },
        {
            "name": "Zaidín",
            "type": "place",
            "geolocation": point(LON - 0.006, LAT - 0.016),
            "geolocation_box": [-3.620, 37.148, -3.590, 37.168],
            "parent_ids": [granada_id, andalucia_id, spain_id],
        },
    ])

    return [spain_id, andalucia_id, granada_id] + neighbourhood_ids

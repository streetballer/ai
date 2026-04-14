from src.common.constants.geo import EARTH_RADIUS_METERS
from src.common.libraries.database import get_database
from src.common.models.place import Place
from src.common.utilities.geo import distance_meters
from src.common.utilities.serialize import serialize_place

SEARCH_RADIUS_METERS = 50000
SEARCH_LIMIT = 20
PLACE_FIELDS_PROJECTION = {"_id": 1, "name": 1, "type": 1, "geolocation": 1, "geolocation_box": 1, "parent_ids": 1}


def search_places(text: str | None, lon: float | None, lat: float | None) -> list[dict]:
    db = get_database()
    has_text = bool(text)
    has_location = lon is not None and lat is not None

    if has_text:
        docs = db.places.get_many({"$text": {"$search": text}}, PLACE_FIELDS_PROJECTION, limit=SEARCH_LIMIT)
        places = [Place.from_doc(doc) for doc in docs]

        if has_location:
            def sort_key(place: Place) -> float:
                if place.geolocation and place.geolocation.get("coordinates"):
                    coords = place.geolocation["coordinates"]
                    return distance_meters(lon, lat, coords[0], coords[1])
                return float("inf")

            places.sort(key=sort_key)
    else:
        radius_radians = SEARCH_RADIUS_METERS / EARTH_RADIUS_METERS
        docs = db.places.get_many(
            {"geolocation": {"$geoWithin": {"$centerSphere": [[lon, lat], radius_radians]}}},
            PLACE_FIELDS_PROJECTION,
            limit=SEARCH_LIMIT,
        )
        places = [Place.from_doc(doc) for doc in docs]

    return [serialize_place(p) for p in places]

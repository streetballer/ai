from src.common.libraries.database import Database
from src.common.models.court import Court
from seed.data.reference import LAT, LON
from seed.helpers.geo import point


def seed_courts(db: Database, place_ids: list[str]) -> list[str]:
    granada_id, centro_id, realejo_id, albaicin_id, zaidin_id = place_ids

    courts = [
        Court(name="Pista del Realejo", geolocation=point(LON, LAT), place_ids=[realejo_id, granada_id]),
        Court(name="Cancha del Albaicín", geolocation=point(LON + 0.009, LAT + 0.007), place_ids=[albaicin_id, granada_id]),
        Court(name="Polideportivo del Centro", geolocation=point(LON + 0.005, LAT + 0.003), place_ids=[centro_id, granada_id]),
        Court(name="Pista de Bib-Rambla", geolocation=point(LON + 0.003, LAT - 0.002), place_ids=[centro_id, granada_id]),
        Court(name="Cancha de Fuentenueva", geolocation=point(LON + 0.012, LAT + 0.005), place_ids=[albaicin_id, granada_id]),
        Court(name="Pista de Zaidín", geolocation=point(LON - 0.006, LAT - 0.016), place_ids=[zaidin_id, granada_id]),
        Court(name="Cancha de La Chana", geolocation=point(LON + 0.007, LAT - 0.012), place_ids=[zaidin_id, granada_id]),
        Court(name="Pista del Arabial", geolocation=point(LON - 0.003, LAT - 0.010), place_ids=[zaidin_id, granada_id]),
        Court(name="Cancha de Cartuja", geolocation=point(LON - 0.002, LAT + 0.010), place_ids=[centro_id, granada_id]),
        Court(name="Pista de los Jardines del Genil", geolocation=point(LON - 0.008, LAT - 0.001), place_ids=[centro_id, granada_id]),
    ]

    return db.courts.insert_many([court.to_doc() for court in courts])

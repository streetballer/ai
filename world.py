from dataclasses import dataclass, field
from io import BytesIO
from json import loads as load_json
from math import asin, atan2, ceil, cos, degrees, exp, log, radians, sin, sqrt
from os.path import isfile
from shutil import copyfileobj
from statistics import median
from typing import Counter
from uuid import uuid4
from zipfile import ZipFile

from requests import get


@dataclass
class Place:
    id: str = field(default_factory=lambda: uuid4().hex, init=False)
    address: dict[str, str]
    geolocation: tuple[float, float]
    geolocation_box: tuple[float, float, float, float]
    population: int
    is_parent: bool = False
    parent_ids: list[str] = field(default_factory=list)


def load_place_data(country: str):

    country = country.strip().lower()
    file_path = "./data/" + country + ".ndjson"

    if not isfile(file_path):
        url = "https://www.geoapify.com/data-share/localities/" + country + ".zip"
        response = get(url)
        if response.status_code == 200:
            with ZipFile(BytesIO(response.content)) as zip:
                zip_files = zip.namelist()
                with open(file_path, "wb") as out_file:
                    for source_file in ["city.ndjson", "town.ndjson"]:
                        for zip_file in zip_files:
                            if source_file in zip_file:
                                with zip.open(zip_file) as in_file:
                                    copyfileobj(in_file, out_file)

    places: list[Place] = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                row = load_json(line)
                address = row.get("address", {})
                for key in list(address.keys()):
                    if "ISO3166" in key or "country_code" in key or "postcode" in key:
                        address.pop(key)
                geolocation = (
                    round(row.get("location")[0], 4),
                    round(row.get("location")[1], 4),
                )
                geolocation_box = (
                    round(row.get("bbox")[0], 4),
                    round(row.get("bbox")[1], 4),
                    round(row.get("bbox")[2], 4),
                    round(row.get("bbox")[3], 4),
                )
                population = round(row.get("population", 0), -2)
                place = Place(address, geolocation, geolocation_box, population)
                places.append(place)
            except Exception as exception:
                print(exception)
                continue

    return sorted(places, key=lambda p: p.population, reverse=True)


def find_place_layers(places: list[Place]):

    layer_keys: list[str] = []

    for address in [place.address for place in places]:
        for key in list(address.keys())[1:]:
            layer_keys.append(key)

    layers = Counter(layer_keys).most_common()
    counts = [count for _, count in layers]
    gaps = [counts[i] - counts[i + 1] for i in range(len(counts) - 1)]
    threshold = gaps.index(max(gaps)) + 1

    layers = [key for key, _ in layers][:threshold]
    layers_sorted = sorted(
        layers,
        key=lambda k: len(set(place.address.get(k, "") for place in places)),
    )

    return layers_sorted


def format_places(places: list[Place], layers: list[str]):

    layers = list(reversed(layers))

    for place in places:
        address = {
            "place": list(place.address.values())[0],
        }
        for key in layers:
            if key in place.address:
                address[key] = (
                    place.address.get(key, "")
                    .replace(" - ", "/")
                    .replace(" — ", "/")
                    .replace(" / ", "/")
                    .replace("/", " / ")
                    .strip()
                )
        place.address = address

    return places


def calculate_geolocation_center(places: list[Place]):

    if len(places) > 0:

        x = y = z = 0.0
        population = sum(p.population for p in places)

        for p in places:
            weight = p.population / population if population > 0 else 1 / len(places)
            lon = radians(p.geolocation[0])
            lat = radians(p.geolocation[1])
            x += cos(lat) * cos(lon) * weight
            y += cos(lat) * sin(lon) * weight
            z += sin(lat) * weight

        if sqrt(x * x + y * y + z * z) > 1e-10:
            longitude = round(degrees(atan2(y, x)), 4)
            latitude = round(degrees(atan2(z, sqrt(x * x + y * y))), 4)
            return (longitude, latitude)


def calculate_geolocation_box(places: list[Place]):

    longitudes: list[float] = []
    latitudes: list[float] = []

    for p in places:
        min_lon, min_lat, max_lon, max_lat = p.geolocation_box
        longitudes.append(min_lon)
        longitudes.append(max_lon)
        latitudes.append(min_lat)
        latitudes.append(max_lat)

    if len(longitudes) > 0 and len(latitudes) > 0:
        return (min(longitudes), min(latitudes), max(longitudes), max(latitudes))


def group_parent_places(places: list[Place], layers: list[str]):
    layer_filters: list[dict[str, str]] = []
    parent_places: list[Place] = []

    for i in range(len(layers)):
        keys = layers[: i + 1]
        for place in places:
            place_filter = {
                key: place.address.get(key, "")
                for key in reversed(keys)
                if key in place.address
            }
            if len(place_filter) > 0 and all(
                any(
                    layer_filter.get(key, "") != place_filter.get(key, "")
                    for key in keys
                )
                for layer_filter in layer_filters
            ):
                layer_filters.append(place_filter)

    for layer_filter in layer_filters:
        filter_places: list[Place] = []
        for place in places:
            if all(
                layer_filter.get(key, "") == place.address.get(key, "")
                for key in layer_filter.keys()
            ):
                filter_places.append(place)
        if len(filter_places) > 0:
            parent_place = Place(
                layer_filter,
                calculate_geolocation_center(filter_places),
                calculate_geolocation_box(filter_places),
                sum(p.population for p in filter_places),
                True,
            )
            parent_places.append(parent_place)

    return sorted(parent_places, key=lambda p: p.population, reverse=True)


def assign_parent_place_ids(places: list[Place]):

    for child in places:

        parents: list[Place] = []
        child_keys = list(child.address.keys())

        for i in range(1, len(child_keys)):

            parent_keys = child_keys[i:] if len(child_keys) > i else []

            if len(parent_keys) > 0:

                for parent in places:

                    if all(
                        parent.address.get(key, "") == child.address.get(key, "")
                        for key in parent_keys
                    ):

                        if len(parent.address) <= len(parent_keys):
                            parents.append(parent)

                for parent in sorted(parents, key=lambda p: len(p.address.keys())):
                    if parent.id not in child.parent_ids:
                        child.parent_ids.append(parent.id)

    return places


def calculate_haversine_km(lon_a: float, lat_a: float, lon_b: float, lat_b: float):
    earth_radius_km = 6371
    delta_lat = radians(lat_b - lat_a)
    delta_lon = radians(lon_b - lon_a)
    a = (
        sin(delta_lat / 2) ** 2
        + cos(radians(lat_a)) * cos(radians(lat_b)) * sin(delta_lon / 2) ** 2
    )
    return 2 * earth_radius_km * asin(sqrt(a))


def calculate_natural_scale_km(places: list[Place]):

    nearest_neighbor_distances = []

    for place in places:
        nearest_distance = None
        for other_place in places:
            if place.id == other_place.id:
                continue
            distance = calculate_haversine_km(
                place.geolocation[0],
                place.geolocation[1],
                other_place.geolocation[0],
                other_place.geolocation[1],
            )
            if nearest_distance is None or distance < nearest_distance:
                nearest_distance = distance
        if nearest_distance is not None:
            nearest_neighbor_distances.append(nearest_distance)

    return float(median(nearest_neighbor_distances))


def calculate_layer_scale_km(places: list[Place], layer: str):

    layer_distances = []

    parents = [p for p in places if p.is_parent and list(p.address.keys())[0] == layer]
    for parent in parents:
        distances_to_parent = []
        children = [p for p in places if not p.is_parent and parent.id in p.parent_ids]
        for child in children:
            distance_to_parent = calculate_haversine_km(
                parent.geolocation[0],
                parent.geolocation[1],
                child.geolocation[0],
                child.geolocation[1],
            )
            distances_to_parent.append(distance_to_parent)
        if len(distances_to_parent) >= 2:
            layer_distance = sum(distances_to_parent) / len(distances_to_parent)
            layer_distances.append(layer_distance)

    return float(median(layer_distances)) if len(layer_distances) > 0 else 0.0


def calculate_zones(places: list[Place], layers: list[str]):

    layer_scales: dict[str, float] = {}
    natural_scale_places = [p for p in places if not p.is_parent]
    layer_scales["place"] = calculate_natural_scale_km(natural_scale_places)
    layers = list(reversed(layers))
    for layer in layers:
        layer_scales[layer] = calculate_layer_scale_km(places, layer)

    zones: dict[str, float] = {}
    new_zones: int = 0

    for i in range(len(layer_scales) - 1):
        keys, values = list[str](layer_scales.keys()), list(layer_scales.values())
        lower_key, lower_scale = keys[i], values[i]
        upper_key, upper_scale = keys[i + 1], values[i + 1]
        scale_growth = upper_scale / lower_scale if lower_scale > 0 else 0
        scale_growth_limit = 4
        zones[lower_key] = round(lower_scale, 2)
        create_zones = ceil(log(scale_growth) / log(scale_growth_limit)) - 1
        if create_zones > 0:
            create_intervals = create_zones + 1
            for i in range(1, create_intervals):
                new_zones += 1
                zone_key = f"zone_{new_zones}"
                zone_scale = lower_scale * exp(
                    i * log(upper_scale / lower_scale) / create_intervals
                )
                zones[zone_key] = round(zone_scale, 2)
        zones[upper_key] = round(upper_scale, 2)

    return zones


countries = ["be", "de", "es", "fr", "gb", "it", "nl", "pt"]

for country in countries:
    print("----")
    print(f"Country: {country.upper()}")
    places = load_place_data(country)
    layers = find_place_layers(places)
    print(f"Administrative Layers: {', '.join(layers)}")
    places = format_places(places, layers)
    print(f"Places: {len(places)}")
    parent_places = group_parent_places(places, layers)
    print(f"Parent Places: {len(parent_places)}")
    places.extend(parent_places)
    places.sort(key=lambda p: p.population, reverse=True)
    places = assign_parent_place_ids(places)
    zones = calculate_zones(places, layers)
    print(f"Zones: {zones}")

    # print_hierarchy_report(scale_sequence, gap_lower, gap_upper, zone_radius

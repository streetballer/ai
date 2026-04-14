from dataclasses import dataclass, field
from io import BytesIO
from json import dump as write_json
from json import loads as read_json
from math import asin, atan2, ceil, cos, degrees, exp, log, radians, sin, sqrt
from os.path import isfile
from re import findall
from shutil import copyfileobj
from statistics import median
from typing import Counter
from uuid import uuid4
from zipfile import ZipFile

import numpy as np
from requests import get
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial import cKDTree

GEOAPIFY_BASE_URL = "https://www.geoapify.com/data-share/localities/"
DATA_ORIGINAL_DIR = "./data/original/"
DATA_PROCESSED_DIR = "./data/processed/"
ZIP_SOURCE_FILES = ["city.ndjson", "town.ndjson"]
ADDRESS_KEYS_TO_STRIP = ["ISO3166", "country_code", "postcode"]
GEOLOCATION_PRECISION = 4
POPULATION_ROUND_FACTOR = -2
EARTH_RADIUS_KM = 6371
MAX_SCALE_GROWTH_FACTOR = 4
CLUSTER_NAME_MAX_COUNT = 3
CLUSTER_NAME_MIN_CUMULATIVE_SHARE = 0.75
CLUSTER_NAME_DROP_RATIO = 3

@dataclass
class Place:
    id: str = field(default_factory=lambda: uuid4().hex, init=False)
    address: dict[str, str]
    geolocation: tuple[float, float]
    geolocation_box: tuple[float, float, float, float]
    population: int
    is_parent: bool = False
    parent_ids: list[str] = field(default_factory=list)


@dataclass
class ProductionPlace:
    id: str
    name: str
    type: str
    geolocation: tuple[float, float]
    geolocation_box: tuple[float, float, float, float]
    parent_ids: list[str]


def list_countries():
    response = get(GEOAPIFY_BASE_URL)
    matches = findall(r'href="([a-z]{2})\.zip"', response.text)
    return sorted(set(matches))


def load_place_data(country: str):
    country = country.strip().lower()
    file_path = DATA_ORIGINAL_DIR + country + ".ndjson"
    if not isfile(file_path):
        url = GEOAPIFY_BASE_URL + country + ".zip"
        response = get(url)
        if response.status_code == 200:
            with ZipFile(BytesIO(response.content)) as zip:
                zip_files = zip.namelist()
                with open(file_path, "wb") as out_file:
                    for source_file in ZIP_SOURCE_FILES:
                        for zip_file in zip_files:
                            if source_file in zip_file:
                                with zip.open(zip_file) as in_file:
                                    copyfileobj(in_file, out_file)
    places: list[Place] = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                row = read_json(line)
                address = row.get("address", {})
                for key in list(address.keys()):
                    if any(strip in key for strip in ADDRESS_KEYS_TO_STRIP):
                        address.pop(key)
                geolocation = (
                    round(row.get("location")[0], GEOLOCATION_PRECISION),
                    round(row.get("location")[1], GEOLOCATION_PRECISION),
                )
                geolocation_box = (
                    round(row.get("bbox")[0], GEOLOCATION_PRECISION),
                    round(row.get("bbox")[1], GEOLOCATION_PRECISION),
                    round(row.get("bbox")[2], GEOLOCATION_PRECISION),
                    round(row.get("bbox")[3], GEOLOCATION_PRECISION),
                )
                population = round(row.get("population", 0), POPULATION_ROUND_FACTOR)
                place = Place(address, geolocation, geolocation_box, population)
                places.append(place)
            except:
                continue
    return places


def sort_places(places: list[Place], layer_order: list[str] | None = None):
    layer_order = layer_order or sorted(
        list(set(list(p.address.keys())[0] for p in places)),
        key=lambda layer: len(
            set(
                p.address.get(layer, "")
                for p in places
                if list(p.address.keys())[0] == layer
            )
        ),
        reverse=True,
    )
    return sorted(
        sorted(places, key=lambda p: p.population, reverse=True),
        key=lambda p: layer_order.index(list(p.address.keys())[0]),
        reverse=True,
    )


def identify_administrative_layers(places: list[Place]):
    layer_keys: list[str] = []
    key_positions: dict[str, list[int]] = {}
    for place in places:
        keys = list(place.address.keys())
        for i in range(1, len(keys)):
            key = keys[i]
            layer_keys.append(key)
            if key not in key_positions:
                key_positions[key] = []
            key_positions[key].append(i)
    layer_key_counter = Counter(layer_keys).most_common()
    counts = [count for _, count in layer_key_counter]
    gaps = [counts[i] - counts[i + 1] for i in range(len(counts) - 1)]
    threshold = gaps.index(max(gaps)) + 1 if len(gaps) > 0 else len(counts)
    layers = [key for key, _ in layer_key_counter][:threshold]
    layers_from_small_to_large = sorted(
        layers,
        key=lambda k: sum(key_positions[k]) / len(key_positions[k]),
    )
    return layers_from_small_to_large


def format_places(places: list[Place], administrative_layers: list[str]):
    for place in places:
        address = {
            "place": list(place.address.values())[0],
        }
        for key in administrative_layers:
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
    if len(places) == 0:
        return None
    longitudes = np.radians([p.geolocation[0] for p in places])
    latitudes = np.radians([p.geolocation[1] for p in places])
    populations = np.array([p.population for p in places], dtype=float)
    total_population = populations.sum()
    weights = (
        populations / total_population
        if total_population > 0
        else np.ones(len(places)) / len(places)
    )
    x = float(np.sum(np.cos(latitudes) * np.cos(longitudes) * weights))
    y = float(np.sum(np.cos(latitudes) * np.sin(longitudes) * weights))
    z = float(np.sum(np.sin(latitudes) * weights))
    if sqrt(x * x + y * y + z * z) > 1e-10:
        longitude = round(degrees(atan2(y, x)), 4)
        latitude = round(degrees(atan2(z, sqrt(x * x + y * y))), 4)
        return (longitude, latitude)


def calculate_geolocation_box(places: list[Place]):
    boxes = np.array([p.geolocation_box for p in places])
    if len(boxes) > 0:
        return (
            float(boxes[:, 0].min()),
            float(boxes[:, 1].min()),
            float(boxes[:, 2].max()),
            float(boxes[:, 3].max()),
        )


def create_parent_places(places: list[Place], administrative_layers: list[str]):
    layer_filters: list[dict[str, str]] = []
    for i in range(len(administrative_layers)):
        keys = administrative_layers[i:]
        for place in places:
            place_filter = {
                key: place.address.get(key, "") for key in keys if key in place.address
            }
            if len(place_filter) > 0 and all(
                (
                    any(
                        layer_filter.get(k, "") != place_filter.get(k, "") for k in keys
                    )
                    or len(layer_filter) != len(place_filter)
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
            places.append(parent_place)
    return places


def assign_parent_places(places: list[Place]):
    parent_lookup: dict[frozenset, Place] = {}
    for place in places:
        if place.is_parent:
            parent_lookup[frozenset(place.address.items())] = place
    for child in places:
        parents: list[Place] = []
        child_keys = list(child.address.keys())
        for i in range(1, len(child_keys)):
            parent_keys = child_keys[i:] if len(child_keys) > i else []
            if len(parent_keys) > 0:
                expected_address = frozenset(
                    (key, child.address.get(key, "")) for key in parent_keys
                )
                parent = parent_lookup.get(expected_address)
                if parent is not None:
                    parents.append(parent)
                for parent in sorted(parents, key=lambda p: len(p.address.keys())):
                    if parent.id not in child.parent_ids:
                        child.parent_ids.append(parent.id)
    return places


def calculate_haversine_km(lon_a: float, lat_a: float, lon_b: float, lat_b: float):
    delta_latitudes = radians(lat_b - lat_a)
    delta_longitudes = radians(lon_b - lon_a)
    a = (
        sin(delta_latitudes / 2) ** 2
        + cos(radians(lat_a)) * cos(radians(lat_b)) * sin(delta_longitudes / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * asin(sqrt(a))


def calculate_natural_scale_km(places: list[Place]):
    lons = np.radians([p.geolocation[0] for p in places])
    lats = np.radians([p.geolocation[1] for p in places])
    coords_3d = np.column_stack(
        [
            np.cos(lats) * np.cos(lons),
            np.cos(lats) * np.sin(lons),
            np.sin(lats),
        ]
    )
    tree = cKDTree(coords_3d)
    distances, _ = tree.query(coords_3d, k=2)
    nearest_distances_3d = distances[:, 1]
    nearest_distances_km = 2 * EARTH_RADIUS_KM * np.arcsin(np.clip(nearest_distances_3d / 2, 0, 1))
    return float(np.median(nearest_distances_km))


def calculate_layer_scale_km(places: list[Place], layer: str):
    children_by_parent: dict[str, list[Place]] = {}
    for place in places:
        if not place.is_parent:
            for parent_id in place.parent_ids:
                if parent_id not in children_by_parent:
                    children_by_parent[parent_id] = []
                children_by_parent[parent_id].append(place)

    layer_distances = []
    parents = [p for p in places if p.is_parent and list(p.address.keys())[0] == layer]
    for parent in parents:
        children = children_by_parent.get(parent.id, [])
        if len(children) < 2:
            continue
        parent_latitudes = np.radians(parent.geolocation[1])
        parent_longitudes = np.radians(parent.geolocation[0])
        child_latitudes = np.radians([c.geolocation[1] for c in children])
        child_longitudes = np.radians([c.geolocation[0] for c in children])
        delta_latitudes = child_latitudes - parent_latitudes
        delta_longitudes = child_longitudes - parent_longitudes
        a = (
            np.sin(delta_latitudes / 2) ** 2
            + np.cos(parent_latitudes)
            * np.cos(child_latitudes)
            * np.sin(delta_longitudes / 2) ** 2
        )
        distances = 2 * EARTH_RADIUS_KM * np.arcsin(np.sqrt(np.clip(a, 0, 1)))
        layer_distances.append(float(distances.mean()))
    return float(median(layer_distances)) if len(layer_distances) > 0 else 0.0


def calculate_zone_requirements(places: list[Place], administrative_layers: list[str]):
    layer_scales: dict[str, float] = {}
    natural_scale_places = [p for p in places if not p.is_parent]
    layer_scales["place"] = calculate_natural_scale_km(natural_scale_places)
    for layer in administrative_layers:
        layer_scales[layer] = calculate_layer_scale_km(places, layer)
    zones: dict[str, float] = {}
    new_zones: int = 0
    for i in range(len(layer_scales) - 1):
        keys, values = list[str](layer_scales.keys()), list(layer_scales.values())
        lower_key, lower_scale = keys[i], values[i]
        upper_key, upper_scale = keys[i + 1], values[i + 1]
        zones[lower_key] = round(lower_scale, 3)
        lower_scale = max(values[: i + 1])
        scale_growth = upper_scale / lower_scale if lower_scale > 0 else 0
        if scale_growth > MAX_SCALE_GROWTH_FACTOR:
            n_zones = ceil(log(scale_growth) / log(MAX_SCALE_GROWTH_FACTOR)) - 1
            if n_zones > 1 and scale_growth > MAX_SCALE_GROWTH_FACTOR * 1.5:
                print(
                    f"Warning: Consecutive custom zones strongly recommended ({round(scale_growth, 1)}x)"
                )
            n_zones = min(n_zones, 1)
            if n_zones > 0:
                create_intervals = n_zones + 1
                for i in range(1, create_intervals):
                    new_zones += 1
                    zone_key = f"zone_{new_zones}"
                    zone_scale = lower_scale * exp(
                        i * log(upper_scale / lower_scale) / create_intervals
                    )
                    zones[zone_key] = round(zone_scale, 3)
        zones[upper_key] = round(upper_scale, 3)
    return zones


def identify_custom_zones(zones: dict[str, float]):
    zone_keys = list(zones.keys())
    custom_zone_keys = [z for z in zone_keys if "zone_" in z]
    custom_zones: dict[str, tuple[str, float, str]] = {}
    for zone_key in custom_zone_keys:
        index = zone_keys.index(zone_key)
        lower_key = zone_keys[index - 1]
        upper_key = zone_keys[index + 1]
        custom_zones[zone_key] = (lower_key, zones[zone_key], upper_key)
    return custom_zones


def cluster_places(places: list[Place], lower_key: str, upper_key: str, scale: float):
    clusters: list[tuple[Place, list[Place]]] = []
    children = [p for p in places if list(p.address.keys())[0] == lower_key]
    parents = [p for p in places if list(p.address.keys())[0] == upper_key]
    for parent in parents:
        parent_keys = list(parent.address.keys())
        zone_places: list[Place] = []
        for child in children:
            if all(parent.address.get(k) == child.address.get(k) for k in parent_keys):
                zone_places.append(child)
        if len(zone_places) < 2:
            continue
        longitudes = np.radians([p.geolocation[0] for p in zone_places])
        latitudes = np.radians([p.geolocation[1] for p in zone_places])
        n = len(zone_places)
        rows = []
        for i in range(n - 1):
            delta_latitudes = latitudes[i + 1 :] - latitudes[i]
            delta_longitudes = longitudes[i + 1 :] - longitudes[i]
            a = (
                np.sin(delta_latitudes / 2) ** 2
                + np.cos(latitudes[i])
                * np.cos(latitudes[i + 1 :])
                * np.sin(delta_longitudes / 2) ** 2
            )
            rows.append(2 * EARTH_RADIUS_KM * np.arcsin(np.sqrt(np.clip(a, 0, 1))))
        zone_candidate_distances = np.concatenate(rows)
        linkage_tree = linkage(zone_candidate_distances, method="average")
        cluster_ids = fcluster(linkage_tree, scale, criterion="distance")
        for cluster_id in set(cluster_ids):
            cluster = sorted(
                [zone_places[i] for i in range(n) if cluster_ids[i] == cluster_id],
                key=lambda p: p.population,
                reverse=True,
            )
            if len(cluster) >= 2:
                clusters.append((parent, cluster))
    return clusters


def name_cluster(cluster: list[Place]):
    name_elements: list[str] = []
    population = sum(p.population for p in cluster)
    if len(cluster) <= 2:
        name_elements = [list(place.address.values())[0] for place in cluster]
    else:
        population_shares = [
            (p.population / population if population > 0 else 1 / len(cluster))
            for p in cluster
        ]
        cumulative_share: float = 0.0
        for i, place in enumerate(cluster):
            name_elements.append(list(place.address.values())[0])
            cumulative_share += population_shares[i]
            if (
                len(name_elements) >= CLUSTER_NAME_MAX_COUNT
                or cumulative_share >= CLUSTER_NAME_MIN_CUMULATIVE_SHARE
                or (
                    i + 1 < len(cluster)
                    and population_shares[i] / population_shares[i + 1]
                    >= CLUSTER_NAME_DROP_RATIO
                )
            ):
                break
    return " + ".join(name_elements)


def create_zones(places: list[Place], zones: dict[str, float]):
    custom_zones = identify_custom_zones(zones)
    for zone_key in list(custom_zones.keys()):
        lower_key, scale, upper_key = custom_zones[zone_key]
        clusters = cluster_places(places, lower_key, upper_key, scale)
        for parent, cluster in clusters:
            address: dict[str, str] = {}
            address[zone_key] = name_cluster(cluster)
            for key in list(parent.address.keys()):
                address[key] = parent.address.get(key, "")
            zone = Place(
                address,
                calculate_geolocation_center(cluster),
                calculate_geolocation_box(cluster),
                sum(p.population for p in cluster),
                True,
                [parent.id] + parent.parent_ids,
            )
            children = [
                place
                for place in places
                if any(p.id in place.parent_ids for p in cluster)
            ]
            for child in cluster + children:
                if zone.id not in child.parent_ids:
                    try:
                        child.parent_ids.insert(
                            child.parent_ids.index(parent.id), zone.id
                        )
                    except Exception as exception:
                        print("----")
                        print(exception)
                        print(parent)
                        print(child)
                        continue
            places.append(zone)
    return places


def convert_places_for_production(places: list[Place]):
    data: list[dict] = []
    for place in places:
        production_place = ProductionPlace(
            place.id,
            list(place.address.values())[0],
            list(place.address.keys())[0],
            place.geolocation,
            place.geolocation_box,
            place.parent_ids,
        ).__dict__
        data.append(production_place)
    return data


countries = list_countries()

for country in countries:
    print("----------------------------------------------------------------")
    try:
        places = load_place_data(country)
        administrative_layers = identify_administrative_layers(places)
        places = format_places(places, administrative_layers)
        places = create_parent_places(places, administrative_layers)
        places = assign_parent_places(places)
        zones = calculate_zone_requirements(places, administrative_layers)
        places = create_zones(places, zones)
        places = sort_places(places, list(zones.keys()))
        data = convert_places_for_production(places)
        with open(DATA_PROCESSED_DIR + country + ".json", "w") as f:
            write_json(data, f, ensure_ascii=False)
        print(
            f"{country.upper()} ({len(places)}): {' - '.join([f'{k} ({round(v, 1)}km)' for k, v in zones.items()])}"
        )
    except Exception as exception:
        print(exception)
        continue

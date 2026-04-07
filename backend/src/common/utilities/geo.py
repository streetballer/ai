from math import radians, sin, cos, sqrt, atan2
from src.common.constants.geo import EARTH_RADIUS_METERS


def distance_meters(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    return EARTH_RADIUS_METERS * 2 * atan2(sqrt(a), sqrt(1 - a))

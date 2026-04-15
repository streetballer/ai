import 'dart:math';

import 'package:streetballer/common/models/geolocation.dart';

const double _earthRadiusMeters = 6371000.0;

/// Returns the haversine distance in metres between two coordinates.
double haversineMeters(Geolocation a, Geolocation b) {
  final lat1 = a.latitude * pi / 180;
  final lat2 = b.latitude * pi / 180;
  final dLat = (b.latitude - a.latitude) * pi / 180;
  final dLon = (b.longitude - a.longitude) * pi / 180;
  final sinDLat = sin(dLat / 2);
  final sinDLon = sin(dLon / 2);
  final x = sinDLat * sinDLat + cos(lat1) * cos(lat2) * sinDLon * sinDLon;
  return 2 * _earthRadiusMeters * atan2(sqrt(x), sqrt(1 - x));
}

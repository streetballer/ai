import 'package:streetballer/common/models/geolocation.dart';

class MapBounds {
  final Geolocation southwest;
  final Geolocation northeast;

  const MapBounds({required this.southwest, required this.northeast});
}

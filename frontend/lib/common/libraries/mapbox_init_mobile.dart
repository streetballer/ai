import 'package:mapbox_maps_flutter/mapbox_maps_flutter.dart';
import 'package:streetballer/common/environment/env.dart';

Future<void> initMapbox() async {
  MapboxOptions.setAccessToken(Env.mapboxToken);
}

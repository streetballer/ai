import 'package:geolocator/geolocator.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'geolocation.g.dart';

class GeolocationLibrary {
  Future<(double longitude, double latitude)?> getCurrentPosition() async {
    var permission = await Geolocator.checkPermission();

    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }

    if (permission == LocationPermission.denied || permission == LocationPermission.deniedForever) {
      return null;
    }

    final position = await Geolocator.getCurrentPosition();
    return (position.longitude, position.latitude);
  }
}

@Riverpod(keepAlive: true)
GeolocationLibrary geolocation(GeolocationRef ref) => GeolocationLibrary();

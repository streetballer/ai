import 'package:geolocator/geolocator.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:streetballer/common/models/geolocation.dart';

part 'geolocation.g.dart';

class GeolocationLibrary {
  Future<Geolocation?> getCurrentPosition() async {
    var permission = await Geolocator.checkPermission();

    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }

    if (permission == LocationPermission.denied || permission == LocationPermission.deniedForever) {
      return null;
    }

    final position = await Geolocator.getCurrentPosition();
    return Geolocation(longitude: position.longitude, latitude: position.latitude);
  }
}

@Riverpod(keepAlive: true)
GeolocationLibrary geolocation(GeolocationRef ref) => GeolocationLibrary();

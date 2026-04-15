import 'package:envied/envied.dart';

part 'env.g.dart';

@Envied(path: '.env', obfuscate: true)
abstract class Env {
  @EnviedField(varName: 'API_BASE_URL')
  static final String apiBaseUrl = _Env.apiBaseUrl;

  @EnviedField(varName: 'MAPBOX_TOKEN')
  static final String mapboxToken = _Env.mapboxToken;

  @EnviedField(varName: 'GOOGLE_MAPS_KEY')
  static final String googleMapsKey = _Env.googleMapsKey;
}

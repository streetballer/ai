import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:streetballer/common/libraries/http_client.dart';
import 'package:streetballer/common/models/court.dart';
import 'package:streetballer/common/models/geolocation.dart';
import 'package:streetballer/common/models/map_bounds.dart';
import 'package:streetballer/common/models/place.dart';
import 'package:streetballer/common/utilities/geo.dart';

part 'map_notifier.g.dart';

class MapState {
  final List<Court> courts;
  final List<Place> placeResults;
  final Place? currentPlace;
  final bool isLoadingCourts;
  final bool isLoadingPlaces;

  const MapState({
    this.courts = const [],
    this.placeResults = const [],
    this.currentPlace,
    this.isLoadingCourts = false,
    this.isLoadingPlaces = false,
  });

  MapState copyWith({
    List<Court>? courts,
    List<Place>? placeResults,
    Place? currentPlace,
    bool clearCurrentPlace = false,
    bool? isLoadingCourts,
    bool? isLoadingPlaces,
  }) {
    return MapState(
      courts: courts ?? this.courts,
      placeResults: placeResults ?? this.placeResults,
      currentPlace: clearCurrentPlace ? null : (currentPlace ?? this.currentPlace),
      isLoadingCourts: isLoadingCourts ?? this.isLoadingCourts,
      isLoadingPlaces: isLoadingPlaces ?? this.isLoadingPlaces,
    );
  }
}

@riverpod
class MapNotifier extends _$MapNotifier {
  Geolocation? _lastSearchCenter;

  @override
  MapState build() => const MapState();

  /// Called by the map widget when the camera has settled. Fetches courts if
  /// the center has drifted more than half the visible diagonal since the last
  /// search, ensuring coverage always exceeds the visible area.
  Future<void> onCameraIdle(Geolocation center, MapBounds bounds) async {
    final diagonal = haversineMeters(bounds.southwest, bounds.northeast);
    final lastCenter = _lastSearchCenter;
    if (lastCenter == null || haversineMeters(center, lastCenter) > diagonal / 2) {
      _lastSearchCenter = center;
      await _fetchCourts(center.longitude, center.latitude, diagonal);
    }
  }

  Future<void> _fetchCourts(double lon, double lat, double radiusMeters) async {
    state = state.copyWith(isLoadingCourts: true);
    final response = await ref.read(backendServiceProvider).get(
      '/courts',
      params: {
        'lon': lon.toString(),
        'lat': lat.toString(),
        'radius': radiusMeters.toStringAsFixed(0),
      },
    );
    if (response == null) {
      state = state.copyWith(isLoadingCourts: false);
      return;
    }
    final courts = (response['courts'] as List<dynamic>)
        .map((c) => Court.fromJson(c as Map<String, dynamic>))
        .toList();
    state = state.copyWith(courts: courts, isLoadingCourts: false);
  }

  Future<void> loadPlace(double lon, double lat) async {
    final response = await ref.read(backendServiceProvider).get(
      '/places',
      params: {'lon': lon.toString(), 'lat': lat.toString()},
    );
    if (response == null) return;
    final places = (response['places'] as List<dynamic>)
        .map((p) => Place.fromJson(p as Map<String, dynamic>))
        .toList();
    if (places.isNotEmpty) {
      state = state.copyWith(currentPlace: places.first);
    }
  }

  Future<void> searchPlaces(String text, {double? lon, double? lat}) async {
    if (text.trim().isEmpty) {
      state = state.copyWith(placeResults: []);
      return;
    }
    state = state.copyWith(isLoadingPlaces: true);
    final params = <String, String>{'text': text};
    if (lon != null) params['lon'] = lon.toString();
    if (lat != null) params['lat'] = lat.toString();
    final response = await ref.read(backendServiceProvider).get('/places', params: params);
    if (response == null) {
      state = state.copyWith(isLoadingPlaces: false);
      return;
    }
    final places = (response['places'] as List<dynamic>)
        .map((p) => Place.fromJson(p as Map<String, dynamic>))
        .toList();
    state = state.copyWith(placeResults: places, isLoadingPlaces: false);
  }

  void selectPlace(Place place) {
    _lastSearchCenter = null;
    state = state.copyWith(currentPlace: place, placeResults: []);
  }

  void clearPlaceResults() {
    state = state.copyWith(placeResults: []);
  }
}

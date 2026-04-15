import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mapbox_maps_flutter/mapbox_maps_flutter.dart';
import 'package:streetballer/common/models/court.dart';
import 'package:streetballer/common/models/geolocation.dart';
import 'package:streetballer/common/models/place.dart';

class PlatformMapView extends StatefulWidget {
  final List<Court> courts;
  final Geolocation? userPosition;
  final Place? targetPlace;
  final void Function(String courtId) onCourtTap;

  const PlatformMapView({
    super.key,
    required this.courts,
    this.userPosition,
    this.targetPlace,
    required this.onCourtTap,
  });

  @override
  State<PlatformMapView> createState() => _PlatformMapViewState();
}

class _PlatformMapViewState extends State<PlatformMapView> {
  MapboxMap? _mapboxMap;
  PointAnnotationManager? _annotationManager;
  List<PointAnnotation> _annotations = [];
  List<Court> _courts = [];
  Uint8List? _courtMarkerImage;

  @override
  void initState() {
    super.initState();
    _loadMarkerImage();
  }

  Future<void> _loadMarkerImage() async {
    final bytes = await rootBundle.load('lib/assets/images/map_court_icon.png');
    if (!mounted) return;
    _courtMarkerImage = bytes.buffer.asUint8List();
    await _updateMarkers(widget.courts);
  }

  @override
  void didUpdateWidget(PlatformMapView oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.courts != oldWidget.courts) {
      _updateMarkers(widget.courts);
    }
    if (widget.targetPlace != oldWidget.targetPlace && widget.targetPlace != null) {
      _flyToPlace(widget.targetPlace!);
    }
  }

  Future<void> _onMapCreated(MapboxMap mapboxMap) async {
    _mapboxMap = mapboxMap;
    _annotationManager = await mapboxMap.annotations.createPointAnnotationManager();
    _annotationManager!.tapEvents(onTap: _onMarkerTap);
    await _updateMarkers(widget.courts);
  }

  Future<void> _updateMarkers(List<Court> courts) async {
    if (_annotationManager == null || _courtMarkerImage == null) return;

    await _annotationManager!.deleteAll();
    _annotations = [];
    _courts = [];

    if (courts.isEmpty) return;

    _courts = courts;
    _annotations = (await _annotationManager!.createMulti(
      courts
          .map((court) => PointAnnotationOptions(
                geometry: Point(
                  coordinates: Position(
                    court.geolocation.longitude,
                    court.geolocation.latitude,
                  ),
                ),
                image: _courtMarkerImage,
                iconSize: 0.15,
              ))
          .toList(),
    ))
        .whereType<PointAnnotation>()
        .toList();
  }

  void _onMarkerTap(PointAnnotation annotation) {
    final index = _annotations.indexWhere((a) => a.id == annotation.id);
    if (index >= 0 && index < _courts.length) {
      widget.onCourtTap(_courts[index].id);
    }
  }

  Future<void> _flyToPlace(Place place) async {
    if (_mapboxMap == null) return;
    await _mapboxMap!.flyTo(
      CameraOptions(
        center: Point(
          coordinates: Position(
            place.geolocation.longitude,
            place.geolocation.latitude,
          ),
        ),
        zoom: 12.0,
      ),
      MapAnimationOptions(duration: 800, startDelay: 0),
    );
  }

  @override
  Widget build(BuildContext context) {
    final position = widget.userPosition;
    return MapWidget(
      key: const ValueKey('streetballer_map'),
      cameraOptions: CameraOptions(
        center: position != null
            ? Point(coordinates: Position(position.longitude, position.latitude))
            : Point(coordinates: Position(0, 20)),
        zoom: position != null ? 13.0 : 1.5,
      ),
      onMapCreated: _onMapCreated,
    );
  }
}

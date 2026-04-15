import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:streetballer/common/models/court.dart';
import 'package:streetballer/common/models/geolocation.dart';
import 'package:streetballer/common/models/map_bounds.dart';
import 'package:streetballer/common/models/place.dart';

class PlatformMapView extends StatefulWidget {
  final List<Court> courts;
  final Geolocation? userPosition;
  final Place? targetPlace;
  final void Function(String courtId) onCourtTap;
  final void Function(Geolocation center, MapBounds bounds) onCameraIdle;

  const PlatformMapView({
    super.key,
    required this.courts,
    this.userPosition,
    this.targetPlace,
    required this.onCourtTap,
    required this.onCameraIdle,
  });

  @override
  State<PlatformMapView> createState() => _PlatformMapViewState();
}

class _PlatformMapViewState extends State<PlatformMapView> {
  GoogleMapController? _controller;
  Set<Marker> _markers = {};

  @override
  void initState() {
    super.initState();
    _updateMarkers(widget.courts);
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

  void _updateMarkers(List<Court> courts) {
    setState(() {
      _markers = courts
          .map((court) => Marker(
                markerId: MarkerId(court.id),
                position: LatLng(
                  court.geolocation.latitude,
                  court.geolocation.longitude,
                ),
                onTap: () => widget.onCourtTap(court.id),
              ))
          .toSet();
    });
  }

  Future<void> _flyToPlace(Place place) async {
    await _controller?.animateCamera(
      CameraUpdate.newLatLngZoom(
        LatLng(place.geolocation.latitude, place.geolocation.longitude),
        12.0,
      ),
    );
  }

  Future<void> _onCameraIdle() async {
    final controller = _controller;
    if (controller == null) return;

    final region = await controller.getVisibleRegion();
    final center = Geolocation(
      longitude: (region.southwest.longitude + region.northeast.longitude) / 2,
      latitude: (region.southwest.latitude + region.northeast.latitude) / 2,
    );
    final bounds = MapBounds(
      southwest: Geolocation(
        longitude: region.southwest.longitude,
        latitude: region.southwest.latitude,
      ),
      northeast: Geolocation(
        longitude: region.northeast.longitude,
        latitude: region.northeast.latitude,
      ),
    );

    widget.onCameraIdle(center, bounds);
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final position = widget.userPosition;
    final initialTarget = position != null
        ? LatLng(position.latitude, position.longitude)
        : const LatLng(20.0, 0.0);

    return GoogleMap(
      initialCameraPosition: CameraPosition(
        target: initialTarget,
        zoom: position != null ? 13.0 : 1.5,
      ),
      markers: _markers,
      onMapCreated: (controller) => _controller = controller,
      onCameraIdle: _onCameraIdle,
      myLocationEnabled: false,
      zoomControlsEnabled: false,
      mapToolbarEnabled: false,
    );
  }
}

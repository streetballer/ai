import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:streetballer/common/constants/spacing.dart';
import 'package:streetballer/common/libraries/geolocation.dart';
import 'package:streetballer/common/models/geolocation.dart' show Geolocation;
import 'package:streetballer/modules/map/logic/map_notifier.dart';
import 'package:streetballer/modules/map/widgets/map_add_court_button.dart';
import 'package:streetballer/modules/map/widgets/map_place_search.dart';
import 'package:streetballer/modules/map/widgets/platform_map.dart';

class MapScreen extends ConsumerStatefulWidget {
  const MapScreen({super.key});

  @override
  ConsumerState<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends ConsumerState<MapScreen> {
  Geolocation? _userPosition;

  @override
  void initState() {
    super.initState();
    _initialize();
  }

  Future<void> _initialize() async {
    final position = await ref.read(geolocationProvider).getCurrentPosition();
    if (!mounted) return;

    if (position != null) {
      setState(() => _userPosition = position);
      await Future.wait<void>([
        ref.read(mapNotifierProvider.notifier).loadCourts(position.longitude, position.latitude),
        ref.read(mapNotifierProvider.notifier).loadPlace(position.longitude, position.latitude),
      ]);
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(mapNotifierProvider);

    return Stack(
      children: [
        Positioned.fill(
          child: PlatformMapView(
            courts: state.courts,
            userPosition: _userPosition,
            targetPlace: state.currentPlace,
            onCourtTap: (courtId) => context.push('/map/$courtId'),
          ),
        ),
        Positioned(
          top: spaceLarge,
          left: spaceLarge,
          right: spaceLarge,
          child: MapPlaceSearch(userPosition: _userPosition),
        ),
        Positioned(
          right: spaceLarge,
          bottom: spaceLarge,
          child: const MapAddCourtButton(),
        ),
      ],
    );
  }
}

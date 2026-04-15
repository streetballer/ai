import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:streetballer/common/constants/borders.dart';
import 'package:streetballer/common/constants/colors.dart';
import 'package:streetballer/common/constants/spacing.dart';
import 'package:streetballer/common/constants/typography.dart';
import 'package:streetballer/common/libraries/localizations/app_localizations.dart';
import 'package:streetballer/common/models/geolocation.dart';
import 'package:streetballer/common/models/place.dart';
import 'package:streetballer/common/widgets/app_icon.dart';
import 'package:streetballer/modules/map/logic/map_notifier.dart';

class MapPlaceSearch extends ConsumerStatefulWidget {
  final Geolocation? userPosition;

  const MapPlaceSearch({super.key, this.userPosition});

  @override
  ConsumerState<MapPlaceSearch> createState() => _MapPlaceSearchState();
}

class _MapPlaceSearchState extends ConsumerState<MapPlaceSearch> {
  final TextEditingController _controller = TextEditingController();
  final FocusNode _focusNode = FocusNode();
  bool _isSearching = false;

  @override
  void initState() {
    super.initState();
    _focusNode.addListener(() {
      setState(() => _isSearching = _focusNode.hasFocus);
      if (!_focusNode.hasFocus) {
        ref.read(mapNotifierProvider.notifier).clearPlaceResults();
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    _focusNode.dispose();
    super.dispose();
  }

  void _onTextChanged(String text) {
    final position = widget.userPosition;
    ref.read(mapNotifierProvider.notifier).searchPlaces(
      text,
      lon: position?.longitude,
      lat: position?.latitude,
    );
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(mapNotifierProvider);
    final l10n = AppLocalizations.of(context);

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          height: 48,
          decoration: BoxDecoration(
            color: colorContainer,
            borderRadius: BorderRadius.circular(borderRadiusMedium),
            border: Border.all(color: colorOutline, width: borderWidthSmall),
          ),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: spaceMedium),
                child: AppIcon('location', size: 20, color: colorMain),
              ),
              Expanded(
                child: TextField(
                  controller: _controller,
                  focusNode: _focusNode,
                  onChanged: _onTextChanged,
                  style: textBodyMedium,
                  decoration: InputDecoration(
                    hintText: state.currentPlace?.name ?? l10n.mapSearchPlaceholder,
                    hintStyle: textBodyMedium.copyWith(
                      color: (_isSearching || state.currentPlace == null)
                          ? colorNeutral
                          : colorForeground,
                    ),
                    border: InputBorder.none,
                    contentPadding: const EdgeInsets.symmetric(vertical: spaceMedium),
                  ),
                ),
              ),
              if (_isSearching)
                GestureDetector(
                  onTap: () {
                    _controller.clear();
                    _focusNode.unfocus();
                  },
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: spaceMedium),
                    child: AppIcon('close_circle', size: 20, color: colorNeutral),
                  ),
                ),
            ],
          ),
        ),
        if (_isSearching && state.placeResults.isNotEmpty) ...[
          const SizedBox(height: spaceSmall),
          Container(
            decoration: BoxDecoration(
              color: colorContainer,
              borderRadius: BorderRadius.circular(borderRadiusMedium),
              border: Border.all(color: colorOutline, width: borderWidthSmall),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                for (int i = 0; i < state.placeResults.length; i++)
                  _PlaceResultItem(
                    place: state.placeResults[i],
                    isLast: i == state.placeResults.length - 1,
                    onTap: () {
                      _controller.clear();
                      _focusNode.unfocus();
                      ref.read(mapNotifierProvider.notifier).selectPlace(state.placeResults[i]);
                    },
                  ),
              ],
            ),
          ),
        ],
      ],
    );
  }
}

class _PlaceResultItem extends StatelessWidget {
  final Place place;
  final bool isLast;
  final VoidCallback onTap;

  const _PlaceResultItem({
    required this.place,
    required this.isLast,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        splashColor: colorMain.withValues(alpha: 0.1),
        highlightColor: colorMain.withValues(alpha: 0.05),
        child: Container(
          width: double.infinity,
          padding: const EdgeInsets.symmetric(
            horizontal: spaceLarge,
            vertical: spaceMedium,
          ),
          decoration: isLast
              ? null
              : const BoxDecoration(
                  border: Border(
                    bottom: BorderSide(color: colorOutline, width: borderWidthSmall),
                  ),
                ),
          child: Row(
            children: [
              AppIcon('location', size: 16, color: colorNeutral),
              const SizedBox(width: spaceSmall),
              Expanded(child: Text(place.name, style: textBodyMedium)),
            ],
          ),
        ),
      ),
    );
  }
}

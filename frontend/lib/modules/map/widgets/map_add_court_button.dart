import 'package:flutter/material.dart';
import 'package:streetballer/common/constants/borders.dart';
import 'package:streetballer/common/constants/colors.dart';
import 'package:streetballer/common/widgets/app_icon.dart';

class MapAddCourtButton extends StatelessWidget {
  const MapAddCourtButton({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 64,
      height: 64,
      child: Material(
        color: colorMain,
        borderRadius: BorderRadius.circular(borderRadiusMedium),
        child: InkWell(
          onTap: () {}, // TODO: open add court flow
          splashColor: Colors.white.withValues(alpha: 0.2),
          highlightColor: Colors.white.withValues(alpha: 0.1),
          borderRadius: BorderRadius.circular(borderRadiusMedium),
          child: const Center(
            child: AppIcon('map_add', size: 24, color: colorBackground),
          ),
        ),
      ),
    );
  }
}

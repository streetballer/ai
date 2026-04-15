import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:streetballer/common/constants/colors.dart';

class AppIcon extends StatelessWidget {
  final String name;
  final double size;
  final Color color;

  const AppIcon(this.name, {super.key, this.size = 24, this.color = colorForeground});

  @override
  Widget build(BuildContext context) {
    return SvgPicture.asset(
      'lib/assets/icons/$name.svg',
      width: size,
      height: size,
      colorFilter: ColorFilter.mode(color, BlendMode.srcIn),
    );
  }
}

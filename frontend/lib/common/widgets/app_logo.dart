import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:streetballer/common/constants/colors.dart';

class AppLogo extends StatelessWidget {
  final double height;
  final Color color;

  const AppLogo({super.key, this.height = 20, this.color = colorForeground});

  @override
  Widget build(BuildContext context) {
    return SvgPicture.asset(
      'lib/assets/images/streetballer_logo.svg',
      height: height,
      colorFilter: ColorFilter.mode(color, BlendMode.srcIn),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:streetballer/common/constants/borders.dart';
import 'package:streetballer/common/constants/colors.dart';
import 'package:streetballer/common/constants/spacing.dart';
import 'package:streetballer/common/constants/typography.dart';

enum AppTagStyle { filled, outlined }

class AppTag extends StatelessWidget {
  final String label;
  final Color color;
  final AppTagStyle style;

  const AppTag({
    super.key,
    required this.label,
    this.color = colorMain,
    this.style = AppTagStyle.outlined,
  });

  @override
  Widget build(BuildContext context) {
    final isFilled = style == AppTagStyle.filled;

    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: spaceMedium,
        vertical: spaceXs,
      ),
      decoration: BoxDecoration(
        color: isFilled ? color : Colors.transparent,
        border: Border.all(color: color, width: borderWidthSmall),
        borderRadius: BorderRadius.circular(borderRadiusSmall),
      ),
      child: Text(
        label,
        style: textBodySmallBold.copyWith(
          color: isFilled ? colorBackground : color,
        ),
      ),
    );
  }
}

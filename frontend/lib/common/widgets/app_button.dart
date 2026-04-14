import 'package:flutter/material.dart';
import 'package:streetballer/common/constants/borders.dart';
import 'package:streetballer/common/constants/colors.dart';
import 'package:streetballer/common/constants/spacing.dart';
import 'package:streetballer/common/constants/typography.dart';

class AppButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;
  final IconData? icon;
  final Color color;
  final bool isLoading;

  const AppButton({
    super.key,
    required this.label,
    this.onPressed,
    this.icon,
    this.color = colorMain,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    return OutlinedButton(
      onPressed: isLoading ? null : onPressed,
      style: ButtonStyle(
        foregroundColor: WidgetStateProperty.resolveWith(
          (states) => states.contains(WidgetState.disabled) ? colorNeutral : color,
        ),
        side: WidgetStateProperty.resolveWith(
          (states) => BorderSide(
            color: states.contains(WidgetState.disabled) ? colorNeutral : color,
            width: borderWidthMedium,
          ),
        ),
        shape: WidgetStateProperty.all(
          RoundedRectangleBorder(borderRadius: BorderRadius.circular(borderRadiusMedium)),
        ),
        minimumSize: WidgetStateProperty.all(const Size(double.infinity, 52)),
        padding: WidgetStateProperty.all(
          const EdgeInsets.symmetric(horizontal: spaceLarge),
        ),
        overlayColor: WidgetStateProperty.all(color.withValues(alpha: 0.1)),
        backgroundColor: WidgetStateProperty.all(Colors.transparent),
      ),
      child: isLoading
          ? SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(color: color, strokeWidth: borderWidthMedium),
            )
          : Row(
              mainAxisAlignment: MainAxisAlignment.center,
              mainAxisSize: MainAxisSize.min,
              children: [
                if (icon case final i?) ...[
                  Icon(i, size: 20),
                  const SizedBox(width: spaceSmall),
                ],
                Text(label, style: textBodyMediumBold),
              ],
            ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:streetballer/common/constants/borders.dart';
import 'package:streetballer/common/constants/colors.dart';
import 'package:streetballer/common/constants/spacing.dart';
import 'package:streetballer/common/constants/typography.dart';
import 'package:streetballer/common/widgets/app_icon.dart';

class AppButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;
  final String? icon;
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
    final bool isDisabled = onPressed == null || isLoading;
    final Color effectiveColor = isDisabled ? colorNeutral : color;

    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: isDisabled ? null : onPressed,
        borderRadius: BorderRadius.circular(borderRadiusMedium),
        splashColor: color.withValues(alpha: 0.1),
        highlightColor: color.withValues(alpha: 0.05),
        child: Container(
          width: double.infinity,
          height: 52,
          padding: const EdgeInsets.symmetric(horizontal: spaceLarge),
          decoration: BoxDecoration(
            border: Border.all(color: effectiveColor, width: borderWidthMedium),
            borderRadius: BorderRadius.circular(borderRadiusMedium),
          ),
          child: Center(
            child: isLoading
                ? SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(
                      color: effectiveColor,
                      strokeWidth: borderWidthMedium,
                    ),
                  )
                : Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      if (icon case final i?) ...[
                        AppIcon(i, size: 20, color: effectiveColor),
                        const SizedBox(width: spaceSmall),
                      ],
                      Text(
                        label,
                        style: textBodyMediumBold.copyWith(color: effectiveColor),
                      ),
                    ],
                  ),
          ),
        ),
      ),
    );
  }
}

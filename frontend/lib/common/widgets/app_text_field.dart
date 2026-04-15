import 'package:flutter/material.dart';
import 'package:streetballer/common/constants/borders.dart';
import 'package:streetballer/common/constants/colors.dart';
import 'package:streetballer/common/constants/spacing.dart';
import 'package:streetballer/common/constants/typography.dart';
import 'package:streetballer/common/widgets/app_icon.dart';

class AppTextField extends StatelessWidget {
  final TextEditingController? controller;
  final String? label;
  final String placeholder;
  final String icon;
  final bool obscureText;
  final TextInputType keyboardType;
  final ValueChanged<String>? onChanged;
  final ValueChanged<String>? onSubmitted;

  const AppTextField({
    super.key,
    this.controller,
    this.label,
    required this.placeholder,
    required this.icon,
    this.obscureText = false,
    this.keyboardType = TextInputType.text,
    this.onChanged,
    this.onSubmitted,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        if (label case final l?) ...[
          Text(l, style: textBodySmall),
          const SizedBox(height: spaceSmall),
        ],
        Container(
          decoration: BoxDecoration(
            color: colorContainer,
            borderRadius: BorderRadius.circular(borderRadiusMedium),
            border: Border.all(color: colorOutline, width: borderWidthSmall),
          ),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Padding(
                padding: const EdgeInsets.only(left: spaceLarge),
                child: AppIcon(icon, size: 20, color: colorNeutral),
              ),
              Expanded(
                child: TextField(
                  controller: controller,
                  obscureText: obscureText,
                  keyboardType: keyboardType,
                  onChanged: onChanged,
                  onSubmitted: onSubmitted,
                  style: textBodyMedium,
                  decoration: InputDecoration(
                    hintText: placeholder,
                    hintStyle: textBodyMedium.copyWith(color: colorNeutral),
                    border: InputBorder.none,
                    contentPadding: const EdgeInsets.symmetric(
                      horizontal: spaceMedium,
                      vertical: spaceLarge,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

import 'package:flutter/material.dart';
import 'package:streetballer/common/constants/spacing.dart';
import 'package:streetballer/common/constants/typography.dart';

class ScreenHeader extends StatelessWidget {
  final String title;
  final Widget? action;

  const ScreenHeader({super.key, required this.title, this.action});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(spaceLarge, spaceLarge, spaceLarge, 0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Text(title, style: textTitle),
          if (action case final a?) a,
        ],
      ),
    );
  }
}

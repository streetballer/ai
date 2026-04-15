import 'package:flutter/material.dart';
import 'package:streetballer/common/constants/colors.dart';
import 'package:streetballer/common/constants/spacing.dart';
import 'package:streetballer/common/constants/typography.dart';

class StreetballerAppBar extends StatelessWidget implements PreferredSizeWidget {
  final Widget? leading;
  final Widget? trailing;

  const StreetballerAppBar({super.key, this.leading, this.trailing});

  @override
  Widget build(BuildContext context) {
    return ColoredBox(
      color: colorBackground,
      child: SizedBox(
        height: kToolbarHeight,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: spaceLarge),
          child: Stack(
            alignment: Alignment.center,
            children: [
              if (leading != null)
                Align(alignment: Alignment.centerLeft, child: leading!),
              Text(
                'Streetballer',
                style: textBodyLargeBold.copyWith(color: colorMain),
              ),
              if (trailing != null)
                Align(alignment: Alignment.centerRight, child: trailing!),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}

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
    return AppBar(
      backgroundColor: colorBackground,
      elevation: 0,
      automaticallyImplyLeading: false,
      leading: leading != null
          ? Padding(
              padding: const EdgeInsets.only(left: spaceLarge),
              child: Align(alignment: Alignment.centerLeft, child: leading),
            )
          : null,
      title: Text('Streetballer', style: textBodyLargeBold.copyWith(color: colorMain)),
      centerTitle: true,
      actions: [
        if (trailing != null)
          Padding(
            padding: const EdgeInsets.only(right: spaceLarge),
            child: Center(child: trailing),
          ),
      ],
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}

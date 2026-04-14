import 'package:flutter/material.dart';
import 'colors.dart';

// Updated to 'DM Sans' once the font asset is added to pubspec.yaml
const String fontFamily = 'DM Sans';

const TextStyle textTitle = TextStyle(
  fontFamily: fontFamily,
  fontSize: 40,
  height: 48 / 40,
  fontWeight: FontWeight.w700,
  color: colorForeground,
);

const TextStyle textHeader = TextStyle(
  fontFamily: fontFamily,
  fontSize: 32,
  height: 40 / 32,
  fontWeight: FontWeight.w700,
  color: colorForeground,
);

const TextStyle textSubheader = TextStyle(
  fontFamily: fontFamily,
  fontSize: 24,
  height: 32 / 24,
  fontWeight: FontWeight.w700,
  color: colorForeground,
);

const TextStyle textBodyLarge = TextStyle(
  fontFamily: fontFamily,
  fontSize: 20,
  height: 24 / 20,
  fontWeight: FontWeight.w400,
  color: colorForeground,
);

const TextStyle textBodyLargeBold = TextStyle(
  fontFamily: fontFamily,
  fontSize: 20,
  height: 24 / 20,
  fontWeight: FontWeight.w700,
  color: colorForeground,
);

const TextStyle textBodyMedium = TextStyle(
  fontFamily: fontFamily,
  fontSize: 16,
  height: 20 / 16,
  fontWeight: FontWeight.w400,
  color: colorForeground,
);

const TextStyle textBodyMediumBold = TextStyle(
  fontFamily: fontFamily,
  fontSize: 16,
  height: 20 / 16,
  fontWeight: FontWeight.w700,
  color: colorForeground,
);

const TextStyle textBodySmall = TextStyle(
  fontFamily: fontFamily,
  fontSize: 12,
  height: 16 / 12,
  fontWeight: FontWeight.w400,
  color: colorForeground,
);

const TextStyle textBodySmallBold = TextStyle(
  fontFamily: fontFamily,
  fontSize: 12,
  height: 16 / 12,
  fontWeight: FontWeight.w700,
  color: colorForeground,
);

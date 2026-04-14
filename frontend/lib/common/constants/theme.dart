import 'package:flutter/material.dart';
import 'colors.dart';
import 'typography.dart';
import 'borders.dart';

final ThemeData appTheme = ThemeData(
  useMaterial3: true,
  brightness: Brightness.dark,
  scaffoldBackgroundColor: colorBackground,
  colorScheme: const ColorScheme.dark(
    primary: colorMain,
    secondary: colorAccent,
    surface: colorContainer,
    onPrimary: colorBackground,
    onSecondary: colorForeground,
    onSurface: colorForeground,
    outline: colorOutline,
    error: colorError,
  ),
  textTheme: const TextTheme(
    displayLarge: textTitle,
    displayMedium: textHeader,
    displaySmall: textSubheader,
    bodyLarge: textBodyLarge,
    bodyMedium: textBodyMedium,
    bodySmall: textBodySmall,
    labelLarge: textBodyMediumBold,
    labelMedium: textBodySmallBold,
  ),
  iconTheme: const IconThemeData(color: colorForeground),
  dividerTheme: const DividerThemeData(color: colorOutline, thickness: 1),
  cardTheme: CardThemeData(
    color: colorContainer,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(borderRadiusMedium),
    ),
  ),
  bottomNavigationBarTheme: const BottomNavigationBarThemeData(
    backgroundColor: colorContainer,
    selectedItemColor: colorMain,
    unselectedItemColor: colorNeutral,
    type: BottomNavigationBarType.fixed,
    showSelectedLabels: true,
    showUnselectedLabels: true,
  ),
);

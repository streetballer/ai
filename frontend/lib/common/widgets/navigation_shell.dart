import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'package:streetballer/common/constants/borders.dart';
import 'package:streetballer/common/constants/colors.dart';
import 'package:streetballer/common/constants/spacing.dart';
import 'package:streetballer/common/constants/typography.dart';
import 'package:streetballer/common/widgets/app_icon.dart';
import 'package:streetballer/common/widgets/app_logo.dart';

// Branch indices — must stay in sync with router.dart
const int _homeBranch = 0;
const int _gamesBranch = 1;
const int _mapBranch = 2;
const int _leagueBranch = 3;
const int _playerBranch = 4;
const int _settingsBranch = 5;

const double _topNavHeight = 48;
const double _bottomNavHeight = 64;

class NavigationShell extends StatelessWidget {
  final StatefulNavigationShell navigationShell;

  const NavigationShell({super.key, required this.navigationShell});

  void _goBranch(int index) {
    navigationShell.goBranch(
      index,
      initialLocation: index == navigationShell.currentIndex,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _TopNavBar(
        currentIndex: navigationShell.currentIndex,
        onPlayerTap: () => _goBranch(_playerBranch),
        onSettingsTap: () => _goBranch(_settingsBranch),
      ),
      body: navigationShell,
      bottomNavigationBar: _BottomNavBar(
        currentIndex: navigationShell.currentIndex,
        onHomeTap: () => _goBranch(_homeBranch),
        onGamesTap: () => _goBranch(_gamesBranch),
        onMapTap: () => _goBranch(_mapBranch),
        onLeagueTap: () => _goBranch(_leagueBranch),
      ),
    );
  }
}

// ── Top nav bar ─────────────────────────────────────────────────────────────

class _TopNavBar extends StatelessWidget implements PreferredSizeWidget {
  final int currentIndex;
  final VoidCallback onPlayerTap;
  final VoidCallback onSettingsTap;

  const _TopNavBar({
    required this.currentIndex,
    required this.onPlayerTap,
    required this.onSettingsTap,
  });

  @override
  Widget build(BuildContext context) {
    return DecoratedBox(
      decoration: const BoxDecoration(
        color: colorContainer,
        border: Border(
          bottom: BorderSide(color: colorOutline, width: borderWidthSmall),
        ),
      ),
      child: SizedBox(
        height: _topNavHeight,
        child: Stack(
          alignment: Alignment.center,
          children: [
            Align(
              alignment: Alignment.centerLeft,
              child: _TopNavButton(
                icon: 'people',
                isActive: currentIndex == _playerBranch,
                onTap: onPlayerTap,
              ),
            ),
            const AppLogo(color: colorNeutral),
            Align(
              alignment: Alignment.centerRight,
              child: _TopNavButton(
                icon: 'settings',
                isActive: currentIndex == _settingsBranch,
                onTap: onSettingsTap,
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(_topNavHeight);
}

class _TopNavButton extends StatelessWidget {
  final String icon;
  final bool isActive;
  final VoidCallback onTap;

  const _TopNavButton({
    required this.icon,
    required this.isActive,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: isActive ? colorBackground : Colors.transparent,
      child: InkWell(
        onTap: onTap,
        splashColor: colorMain.withValues(alpha: 0.1),
        highlightColor: colorMain.withValues(alpha: 0.05),
        child: SizedBox(
          width: _topNavHeight,
          height: _topNavHeight,
          child: Center(
            child: AppIcon(
              icon,
              color: isActive ? colorMain : colorNeutral,
            ),
          ),
        ),
      ),
    );
  }
}

// ── Bottom nav bar ───────────────────────────────────────────────────────────

class _BottomNavBar extends StatelessWidget {
  final int currentIndex;
  final VoidCallback onHomeTap;
  final VoidCallback onGamesTap;
  final VoidCallback onMapTap;
  final VoidCallback onLeagueTap;

  const _BottomNavBar({
    required this.currentIndex,
    required this.onHomeTap,
    required this.onGamesTap,
    required this.onMapTap,
    required this.onLeagueTap,
  });

  @override
  Widget build(BuildContext context) {
    return DecoratedBox(
      decoration: const BoxDecoration(
        color: colorContainer,
        border: Border(
          top: BorderSide(color: colorOutline, width: borderWidthSmall),
        ),
      ),
      child: SafeArea(
        top: false,
        child: SizedBox(
          height: _bottomNavHeight,
          child: Row(
            children: [
              Expanded(
                child: _BottomNavItem(
                  label: 'Home',
                  icon: 'house',
                  isActive: currentIndex == _homeBranch,
                  onTap: onHomeTap,
                ),
              ),
              Expanded(
                child: _BottomNavItem(
                  label: 'Games',
                  icon: 'basketball',
                  isActive: currentIndex == _gamesBranch,
                  onTap: onGamesTap,
                ),
              ),
              const SizedBox(width: spaceMedium),
              _QrButton(),
              const SizedBox(width: spaceMedium),
              Expanded(
                child: _BottomNavItem(
                  label: 'Map',
                  icon: 'map',
                  isActive: currentIndex == _mapBranch,
                  onTap: onMapTap,
                ),
              ),
              Expanded(
                child: _BottomNavItem(
                  label: 'League',
                  icon: 'trophy',
                  isActive: currentIndex == _leagueBranch,
                  onTap: onLeagueTap,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _BottomNavItem extends StatelessWidget {
  final String label;
  final String icon;
  final bool isActive;
  final VoidCallback onTap;

  const _BottomNavItem({
    required this.label,
    required this.icon,
    required this.isActive,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final Color color = isActive ? colorMain : colorNeutral;

    return Material(
      color: isActive ? colorBackground : Colors.transparent,
      child: InkWell(
        onTap: onTap,
        splashColor: colorMain.withValues(alpha: 0.1),
        highlightColor: colorMain.withValues(alpha: 0.05),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            AppIcon(icon, size: 24, color: color),
            const SizedBox(height: spaceXs),
            Text(label, style: textBodySmallBold.copyWith(color: color)),
          ],
        ),
      ),
    );
  }
}

class _QrButton extends StatelessWidget {
  const _QrButton();

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: _bottomNavHeight,
      child: Material(
        color: colorMain,
        child: InkWell(
          onTap: () => context.push('/qr'),
          splashColor: Colors.white.withValues(alpha: 0.2),
          highlightColor: Colors.white.withValues(alpha: 0.1),
          child: const Center(
            child: AppIcon('qr', size: 24, color: colorBackground),
          ),
        ),
      ),
    );
  }
}

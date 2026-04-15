import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

import 'package:streetballer/common/widgets/navigation_shell.dart';
import 'package:streetballer/modules/authentication/screens/authentication_screen.dart';
import 'package:streetballer/modules/courts/screens/court_screen.dart';
import 'package:streetballer/modules/games/screens/games_screen.dart';
import 'package:streetballer/modules/home/screens/home_screen.dart';
import 'package:streetballer/modules/league/screens/league_screen.dart';
import 'package:streetballer/modules/map/screens/map_screen.dart';
import 'package:streetballer/modules/players/screens/player_screen.dart';
import 'package:streetballer/modules/qr/screens/qr_screen.dart';
import 'package:streetballer/modules/score/screens/score_screen.dart';
import 'package:streetballer/modules/settings/screens/settings_screen.dart';

part 'router.g.dart';

@Riverpod(keepAlive: true)
GoRouter router(RouterRef ref) {
  return GoRouter(
    initialLocation: '/home',
    routes: [
      StatefulShellRoute.indexedStack(
        builder: (context, state, navigationShell) =>
            NavigationShell(navigationShell: navigationShell),
        branches: [
          // Branch 0: Home
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/home',
              builder: (context, state) => const HomeScreen(),
            ),
          ]),
          // Branch 1: Games
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/games',
              builder: (context, state) => const GamesScreen(),
            ),
          ]),
          // Branch 2: Map (with Court child)
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/map',
              builder: (context, state) => const MapScreen(),
              routes: [
                GoRoute(
                  path: ':courtId',
                  builder: (context, state) =>
                      CourtScreen(courtId: state.pathParameters['courtId']!),
                ),
              ],
            ),
          ]),
          // Branch 3: League (with Score child)
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/league',
              builder: (context, state) => const LeagueScreen(),
              routes: [
                GoRoute(
                  path: ':scoreId',
                  builder: (context, state) =>
                      ScoreScreen(scoreId: state.pathParameters['scoreId']!),
                ),
              ],
            ),
          ]),
          // Branch 4: Player (own profile via top nav; any player via deep link)
          StatefulShellBranch(
            initialLocation: '/players/me',
            routes: [
              GoRoute(
                path: '/players/:playerId',
                builder: (context, state) =>
                    PlayerScreen(playerId: state.pathParameters['playerId']!),
              ),
            ],
          ),
          // Branch 5: Settings
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/settings',
              builder: (context, state) => const SettingsScreen(),
            ),
          ]),
        ],
      ),
      // Fullscreen modals (no nav bars)
      GoRoute(
        path: '/qr',
        pageBuilder: (context, state) => const MaterialPage(
          fullscreenDialog: true,
          child: QrScreen(),
        ),
      ),
      GoRoute(
        path: '/authentication',
        pageBuilder: (context, state) => const MaterialPage(
          fullscreenDialog: true,
          child: AuthenticationScreen(),
        ),
      ),
    ],
  );
}

import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

import 'package:streetballer/common/widgets/navigation_shell.dart';
import 'package:streetballer/modules/authentication/screens/authentication_screen.dart';
import 'package:streetballer/modules/courts/screens/court_screen.dart';
import 'package:streetballer/modules/courts/screens/courts_screen.dart';
import 'package:streetballer/modules/games/screens/games_screen.dart';
import 'package:streetballer/modules/home/screens/home_screen.dart';
import 'package:streetballer/modules/league/screens/league_screen.dart';
import 'package:streetballer/modules/players/screens/player_screen.dart';
import 'package:streetballer/modules/players/screens/players_screen.dart';
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
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/home',
              builder: (context, state) => const HomeScreen(),
            ),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/games',
              builder: (context, state) => const GamesScreen(),
            ),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/courts',
              builder: (context, state) => const CourtsScreen(),
            ),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/league',
              builder: (context, state) => const LeagueScreen(),
            ),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/players',
              builder: (context, state) => const PlayersScreen(),
            ),
          ]),
        ],
      ),
      GoRoute(
        path: '/courts/:courtId',
        builder: (context, state) =>
            CourtScreen(courtId: state.pathParameters['courtId']!),
      ),
      GoRoute(
        path: '/players/:playerId',
        builder: (context, state) =>
            PlayerScreen(playerId: state.pathParameters['playerId']!),
      ),
      GoRoute(
        path: '/score/:scoreId',
        builder: (context, state) =>
            ScoreScreen(scoreId: state.pathParameters['scoreId']!),
      ),
      GoRoute(
        path: '/settings',
        builder: (context, state) => const SettingsScreen(),
      ),
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

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:streetballer/common/constants/theme.dart';
import 'package:streetballer/common/libraries/mapbox_init.dart';
import 'package:streetballer/common/libraries/localizations/app_localizations.dart';
import 'package:streetballer/common/routes/router.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initMapbox();
  runApp(const ProviderScope(child: App()));
}

class App extends ConsumerWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MaterialApp.router(
      title: 'Streetballer',
      theme: appTheme,
      routerConfig: ref.watch(routerProvider),
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      supportedLocales: AppLocalizations.supportedLocales,
    );
  }
}

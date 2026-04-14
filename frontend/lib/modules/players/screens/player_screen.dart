import 'package:flutter/material.dart';

class PlayerScreen extends StatelessWidget {
  final String playerId;

  const PlayerScreen({super.key, required this.playerId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Center(child: Text('Player $playerId')),
    );
  }
}

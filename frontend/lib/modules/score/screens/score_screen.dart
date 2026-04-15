import 'package:flutter/material.dart';

class ScoreScreen extends StatelessWidget {
  final String scoreId;

  const ScoreScreen({super.key, required this.scoreId});

  @override
  Widget build(BuildContext context) {
    return Center(child: Text('Score $scoreId'));
  }
}

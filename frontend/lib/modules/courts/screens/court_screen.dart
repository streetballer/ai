import 'package:flutter/material.dart';

class CourtScreen extends StatelessWidget {
  final String courtId;

  const CourtScreen({super.key, required this.courtId});

  @override
  Widget build(BuildContext context) {
    return Center(child: Text('Court $courtId'));
  }
}

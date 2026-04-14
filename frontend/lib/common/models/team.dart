import 'package:streetballer/common/models/geolocation.dart';

class Team {
  final String id;
  final String color;
  final Geolocation geolocation;
  final String courtId;
  final DateTime lastActivity;

  const Team({
    required this.id,
    required this.color,
    required this.geolocation,
    required this.courtId,
    required this.lastActivity,
  });

  factory Team.fromJson(Map<String, dynamic> json) {
    return Team(
      id: json['_id'] as String,
      color: json['color'] as String,
      geolocation: Geolocation.fromJson(json['geolocation'] as Map<String, dynamic>),
      courtId: json['court_id'] as String,
      lastActivity: DateTime.parse(json['last_activity'] as String),
    );
  }
}

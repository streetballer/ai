import 'package:streetballer/common/models/geolocation.dart';

class Score {
  final String id;
  final DateTime timestamp;
  final List<int> result;
  final List<int> points;
  final List<List<String>> players;
  final List<String> teams;
  final List<String> colors;
  final List<String> confirmations;
  final List<String> rejections;
  final bool confirmed;
  final List<String> playerIds;
  final Geolocation? geolocation;
  final String courtId;
  final List<String> placeIds;

  const Score({
    required this.id,
    required this.timestamp,
    required this.result,
    required this.points,
    required this.players,
    required this.teams,
    required this.colors,
    required this.confirmations,
    required this.rejections,
    required this.confirmed,
    required this.playerIds,
    this.geolocation,
    required this.courtId,
    required this.placeIds,
  });

  factory Score.fromJson(Map<String, dynamic> json) {
    final geo = json['geolocation'];
    return Score(
      id: json['_id'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
      result: List<int>.from(json['result'] as List<dynamic>),
      points: List<int>.from(json['points'] as List<dynamic>),
      players: (json['players'] as List<dynamic>)
          .map((side) => List<String>.from(side as List<dynamic>))
          .toList(),
      teams: List<String>.from(json['teams'] as List<dynamic>),
      colors: List<String>.from(json['colors'] as List<dynamic>),
      confirmations: List<String>.from(json['confirmations'] as List<dynamic>),
      rejections: List<String>.from(json['rejections'] as List<dynamic>),
      confirmed: json['confirmed'] as bool,
      playerIds: List<String>.from(json['player_ids'] as List<dynamic>),
      geolocation: geo != null ? Geolocation.fromJson(geo as Map<String, dynamic>) : null,
      courtId: json['court_id'] as String,
      placeIds: List<String>.from(json['place_ids'] as List<dynamic>),
    );
  }
}

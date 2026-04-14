class Game {
  final String id;
  final DateTime timestamp;
  final String courtId;
  final List<String> playerIds;

  const Game({
    required this.id,
    required this.timestamp,
    required this.courtId,
    required this.playerIds,
  });

  factory Game.fromJson(Map<String, dynamic> json) {
    return Game(
      id: json['_id'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
      courtId: json['court_id'] as String,
      playerIds: List<String>.from(json['player_ids'] as List<dynamic>),
    );
  }
}

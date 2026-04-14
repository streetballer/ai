import 'package:streetballer/common/models/geolocation.dart';

class Player {
  final String id;
  final String username;
  final String? teamId;

  // Private fields — only present when fetching own player data
  final String? email;
  final bool? emailVerified;
  final String? language;
  final Geolocation? geolocation;

  const Player({
    required this.id,
    required this.username,
    this.teamId,
    this.email,
    this.emailVerified,
    this.language,
    this.geolocation,
  });

  factory Player.fromJson(Map<String, dynamic> json) {
    final geo = json['geolocation'];
    return Player(
      id: json['_id'] as String,
      username: json['username'] as String,
      teamId: json['team_id'] as String?,
      email: json['email'] as String?,
      emailVerified: json['email_verified'] as bool?,
      language: json['language'] as String?,
      geolocation: geo != null ? Geolocation.fromJson(geo as Map<String, dynamic>) : null,
    );
  }
}

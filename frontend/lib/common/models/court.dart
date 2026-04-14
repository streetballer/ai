import 'package:streetballer/common/models/geolocation.dart';

class Court {
  final String id;
  final String name;
  final Geolocation geolocation;
  final List<String> placeIds;

  const Court({
    required this.id,
    required this.name,
    required this.geolocation,
    required this.placeIds,
  });

  factory Court.fromJson(Map<String, dynamic> json) {
    return Court(
      id: json['_id'] as String,
      name: json['name'] as String,
      geolocation: Geolocation.fromJson(json['geolocation'] as Map<String, dynamic>),
      placeIds: List<String>.from(json['place_ids'] as List<dynamic>),
    );
  }
}

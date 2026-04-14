import 'package:streetballer/common/models/geolocation.dart';

class Place {
  final String id;
  final String name;
  final String type;
  final Geolocation geolocation;
  final List<double> geolocationBox;
  final List<String> parentIds;

  const Place({
    required this.id,
    required this.name,
    required this.type,
    required this.geolocation,
    required this.geolocationBox,
    required this.parentIds,
  });

  factory Place.fromJson(Map<String, dynamic> json) {
    return Place(
      id: json['_id'] as String,
      name: json['name'] as String,
      type: json['type'] as String,
      geolocation: Geolocation.fromJson(json['geolocation'] as Map<String, dynamic>),
      geolocationBox: List<double>.from(
        (json['geolocation_box'] as List<dynamic>).map((v) => (v as num).toDouble()),
      ),
      parentIds: List<String>.from(json['parent_ids'] as List<dynamic>),
    );
  }
}

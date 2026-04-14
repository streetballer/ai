class Geolocation {
  final double longitude;
  final double latitude;

  const Geolocation({required this.longitude, required this.latitude});

  factory Geolocation.fromJson(Map<String, dynamic> json) {
    final coordinates = json['coordinates'] as List<dynamic>;
    return Geolocation(
      longitude: (coordinates[0] as num).toDouble(),
      latitude: (coordinates[1] as num).toDouble(),
    );
  }
}

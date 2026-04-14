abstract class BackendService {
  Future<Map<String, dynamic>?> get(String path, {Map<String, String>? params});
  Future<Map<String, dynamic>?> post(String path, {Map<String, dynamic>? body});
}

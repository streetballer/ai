import 'package:dio/dio.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:streetballer/common/constants/storage_keys.dart';
import 'package:streetballer/common/environment/env.dart';
import 'package:streetballer/common/libraries/secure_storage.dart';
import 'package:streetballer/common/services/backend_service.dart';
import 'package:streetballer/common/services/storage_service.dart';

part 'http_client.g.dart';

class HttpBackendService implements BackendService {
  final Dio _dio;
  final StorageService _storage;

  HttpBackendService(this._storage)
      : _dio = Dio(BaseOptions(baseUrl: Env.apiBaseUrl)) {
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = await _storage.get(storageKeyAccessToken);
        if (token != null) options.headers['Authorization'] = 'Bearer $token';
        handler.next(options);
      },
      onError: (error, handler) async {
        final isUnauthorized = error.response?.statusCode == 401;
        final alreadyRetried = error.requestOptions.extra['_retried'] == true;

        if (isUnauthorized && !alreadyRetried && await _refreshTokens()) {
          final token = await _storage.get(storageKeyAccessToken);
          final opts = Options(
            method: error.requestOptions.method,
            headers: {...error.requestOptions.headers, if (token != null) 'Authorization': 'Bearer $token'},
            extra: {'_retried': true},
          );
          try {
            final response = await _dio.request(
              error.requestOptions.path,
              data: error.requestOptions.data,
              queryParameters: error.requestOptions.queryParameters,
              options: opts,
            );
            handler.resolve(response);
            return;
          } catch (_) {}
        }

        handler.next(error);
      },
    ));
  }

  Future<bool> _refreshTokens() async {
    final refreshToken = await _storage.get(storageKeyRefreshToken);
    if (refreshToken == null) return false;

    try {
      final response = await Dio(BaseOptions(baseUrl: Env.apiBaseUrl))
          .post('/auth/refresh/$refreshToken');
      final data = response.data['data'] as Map<String, dynamic>?;
      final accessToken = data?['access_token'] as String?;
      final newRefreshToken = data?['refresh_token'] as String?;

      if (accessToken == null || newRefreshToken == null) return false;

      await _storage.set(storageKeyAccessToken, accessToken);
      await _storage.set(storageKeyRefreshToken, newRefreshToken);
      return true;
    } catch (_) {
      await _storage.delete(storageKeyAccessToken);
      await _storage.delete(storageKeyRefreshToken);
      return false;
    }
  }

  Map<String, dynamic>? _parseResponse(Response response) {
    if (response.statusCode != null &&
        response.statusCode! >= 200 &&
        response.statusCode! < 300) {
      return response.data['data'] as Map<String, dynamic>? ?? {};
    }
    return null;
  }

  @override
  Future<Map<String, dynamic>?> get(String path, {Map<String, String>? params}) async {
    try {
      final response = await _dio.get(path, queryParameters: params);
      return _parseResponse(response);
    } on DioException {
      return null;
    }
  }

  @override
  Future<Map<String, dynamic>?> post(String path, {Map<String, dynamic>? body}) async {
    try {
      final response = await _dio.post(path, data: body);
      return _parseResponse(response);
    } on DioException {
      return null;
    }
  }
}

@Riverpod(keepAlive: true)
BackendService backendService(BackendServiceRef ref) {
  return HttpBackendService(ref.watch(storageServiceProvider));
}

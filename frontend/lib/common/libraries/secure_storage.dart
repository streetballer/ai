import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:streetballer/common/services/storage_service.dart';

part 'secure_storage.g.dart';

class SecureStorageService implements StorageService {
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  @override
  Future<String?> get(String key) => _storage.read(key: key);

  @override
  Future<void> set(String key, String value) => _storage.write(key: key, value: value);

  @override
  Future<void> delete(String key) => _storage.delete(key: key);

  @override
  Future<void> clear() => _storage.deleteAll();
}

@Riverpod(keepAlive: true)
StorageService storageService(StorageServiceRef ref) => SecureStorageService();

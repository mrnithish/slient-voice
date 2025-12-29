import 'dart:io';
import 'package:dio/dio.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'auth_service.dart';

class ApiService {
  final Dio _dio = Dio();
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  final String _baseUrl;
  
  ApiService() : _baseUrl = dotenv.env['API_BASE_URL'] ?? 'http://localhost:8000' {
    _dio.options.baseUrl = _baseUrl;
    _dio.options.connectTimeout = const Duration(seconds: 30);
    _dio.options.receiveTimeout = const Duration(seconds: 30);
    
    // Add interceptor for JWT token
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = await _storage.read(key: 'jwt_token');
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
    ));
  }
  
  Future<Map<String, dynamic>> uploadVoiceEntry(File audioFile) async {
    try {
      final formData = FormData.fromMap({
        'audio': await MultipartFile.fromFile(
          audioFile.path,
          filename: audioFile.path.split('/').last,
        ),
      });
      
      final response = await _dio.post(
        '/entry/upload',
        data: formData,
        options: Options(
          contentType: 'multipart/form-data',
        ),
      );
      
      return response.data;
    } catch (e) {
      print('Error uploading voice entry: $e');
      rethrow;
    }
  }
  
  Future<List<Map<String, dynamic>>> getVoiceEntries({
    int limit = 50,
    int skip = 0,
  }) async {
    try {
      final response = await _dio.get(
        '/entry/list',
        queryParameters: {
          'limit': limit,
          'skip': skip,
        },
      );
      
      return List<Map<String, dynamic>>.from(response.data['entries']);
    } catch (e) {
      print('Error fetching voice entries: $e');
      rethrow;
    }
  }
  
  Future<Map<String, dynamic>> getVoiceEntry(String entryId) async {
    try {
      final response = await _dio.get('/entry/$entryId');
      return response.data;
    } catch (e) {
      print('Error fetching voice entry: $e');
      rethrow;
    }
  }
}




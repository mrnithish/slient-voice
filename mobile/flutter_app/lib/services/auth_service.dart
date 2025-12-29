import 'package:flutter/material.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class AuthService extends ChangeNotifier {
  final GoogleSignIn _googleSignIn = GoogleSignIn(
    scopes: ['email', 'profile'],
  );
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  
  String? _token;
  Map<String, dynamic>? _user;
  bool _isLoading = false;
  
  String? get token => _token;
  Map<String, dynamic>? get user => _user;
  bool get isAuthenticated => _token != null;
  bool get isLoading => _isLoading;
  
  AuthService() {
    _loadStoredToken();
  }
  
  Future<void> _loadStoredToken() async {
    try {
      _token = await _storage.read(key: 'jwt_token');
      final userStr = await _storage.read(key: 'user_data');
      if (userStr != null) {
        _user = json.decode(userStr);
      }
      notifyListeners();
    } catch (e) {
      print('Error loading stored token: $e');
    }
  }
  
  Future<bool> signInWithGoogle() async {
    try {
      _isLoading = true;
      notifyListeners();
      
      // Sign in with Google
      final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();
      
      if (googleUser == null) {
        _isLoading = false;
        notifyListeners();
        return false; // User cancelled
      }
      
      // Get authentication details
      final GoogleSignInAuthentication googleAuth = await googleUser.authentication;
      
      if (googleAuth.idToken == null) {
        _isLoading = false;
        notifyListeners();
        return false;
      }
      
      // Send ID token to backend
      final apiBaseUrl = dotenv.env['API_BASE_URL'] ?? 'http://localhost:8000';
      final response = await http.post(
        Uri.parse('$apiBaseUrl/auth/google'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'id_token': googleAuth.idToken}),
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _token = data['access_token'];
        _user = data['user'];
        
        // Store token and user data securely
        await _storage.write(key: 'jwt_token', value: _token);
        await _storage.write(key: 'user_data', value: json.encode(_user));
        
        _isLoading = false;
        notifyListeners();
        return true;
      } else {
        _isLoading = false;
        notifyListeners();
        return false;
      }
    } catch (e) {
      print('Error signing in: $e');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }
  
  Future<void> signOut() async {
    try {
      await _googleSignIn.signOut();
      await _storage.delete(key: 'jwt_token');
      await _storage.delete(key: 'user_data');
      _token = null;
      _user = null;
      notifyListeners();
    } catch (e) {
      print('Error signing out: $e');
    }
  }
}




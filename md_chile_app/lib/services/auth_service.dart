import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class AuthService {
  final String baseUrl = "http://127.0.0.1:8000/api/";
  static String? accessToken;
  static Map<String, dynamic>? userData; // AQUÍ SE GUARDARÁ EL NOMBRE Y FOTO REAL

  Future<bool> login(String email, String password) async {
    try {
      // 1. Pedimos el Token
      final tokenRes = await http.post(
        Uri.parse("${baseUrl}token/"),
        body: {'username': email, 'password': password},
      );

      if (tokenRes.statusCode == 200) {
        accessToken = json.decode(tokenRes.body)['access'];

        // 2. PEDIMOS LOS DATOS REALES (NOMBRE, FOTO, PUNTOS)
        // Debes tener este endpoint creado en Django (UserProfileAPIView)
        final profileRes = await http.get(
          Uri.parse("${baseUrl}user/profile/"),
          headers: {'Authorization': 'Bearer $accessToken'},
        );

        if (profileRes.statusCode == 200) {
          userData = json.decode(profileRes.body);
          debugPrint("✅ Datos reales cargados: ${userData?['full_name']}");
          return true;
        }
      }
      return false;
    } catch (e) {
      debugPrint("❌ Error: $e");
      return false;
    }
  }
}
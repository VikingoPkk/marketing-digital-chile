import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  // Dirección del servidor Django
  static const String baseUrl = "http://127.0.0.1:8000/api";

  // CABECERAS DINÁMICAS: Recupera el Token real para cada petición de forma segura
  static Future<Map<String, String>> get _headers async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('auth_token');
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  /// Protocolo de Ingreso Real (Login)
  static Future<bool> login(String email, String password) async {
    try {
      final respuesta = await http.post(
        Uri.parse('$baseUrl/login/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'password': password}),
      );

      if (respuesta.statusCode == 200) {
        final datos = jsonDecode(respuesta.body);
        final prefs = await SharedPreferences.getInstance();
        // Sella la identidad en la bóveda local
        await prefs.setString('auth_token', datos['token']);
        return true;
      }
    } catch (e) {
      // Error silencioso para producción
    }
    return false;
  }

  /// Extrae foto y nombre reales del usuario (Angelo Wilche H)
  static Future<Map<String, dynamic>> obtenerPerfilUsuario() async {
    try {
      final h = await _headers;
      final respuesta = await http.get(Uri.parse('$baseUrl/perfil/'), headers: h);
      return respuesta.statusCode == 200 ? json.decode(respuesta.body) : {};
    } catch (e) {
      return {};
    }
  }

  /// Trae los cursos que el usuario ya compró
  static Future<List<dynamic>> obtenerCursosPropios() async {
    try {
      final h = await _headers;
      final respuesta = await http.get(Uri.parse('$baseUrl/mis-cursos/'), headers: h);
      return respuesta.statusCode == 200 ? json.decode(respuesta.body) : [];
    } catch (e) {
      return [];
    }
  }

  /// Trae los cursos disponibles para la venta en la tienda
  static Future<List<dynamic>> obtenerCursosTienda() async {
    try {
      final h = await _headers;
      final respuesta = await http.get(Uri.parse('$baseUrl/tienda/'), headers: h);
      return respuesta.statusCode == 200 ? json.decode(respuesta.body) : [];
    } catch (e) {
      return [];
    }
  }

  /// Obtiene las lecciones de un curso específico para el visor de estudio
  static Future<List<dynamic>> obtenerLecciones(int cursoId) async {
    try {
      final h = await _headers;
      final respuesta = await http.get(
        Uri.parse('$baseUrl/cursos/$cursoId/lecciones/'), 
        headers: h
      );
      return respuesta.statusCode == 200 ? json.decode(respuesta.body) : [];
    } catch (e) {
      return [];
    }
  }
}
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // La dirección de su servidor local
  static const String baseUrl = "http://127.0.0.1:8000/api";

  static Future<List<dynamic>> obtenerCursos() async {
    final url = Uri.parse('$baseUrl/cursos/');
    try {
      final respuesta = await http.get(url);
      if (respuesta.statusCode == 200) {
        return json.decode(respuesta.body);
      }
    } catch (e) {
      print("Error de conexión con el reactor Django: $e");
    }
    return [];
  }
}
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../services/auth_service.dart';

class CoursesScreen extends StatefulWidget {
  const CoursesScreen({super.key});
  @override State<CoursesScreen> createState() => _CoursesScreenState();
}

class _CoursesScreenState extends State<CoursesScreen> {
  List courses = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadCourses();
  }

  Future<void> _loadCourses() async {
    try {
      final response = await http.get(
        Uri.parse("http://127.0.0.1:8000/api/cursos/"),
        headers: {
          if (AuthService.accessToken != null) 
            'Authorization': 'Bearer ${AuthService.accessToken}',
        },
      );

      if (response.statusCode == 200) {
        setState(() {
          courses = json.decode(response.body);
          isLoading = false;
        });
      }
    } catch (e) {
      debugPrint("Error cargando cursos: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) return const Center(child: CircularProgressIndicator());

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: courses.length,
      itemBuilder: (context, index) {
        final curso = courses[index];
        bool isPurchased = curso['is_purchased'] ?? false; 

        return Card(
          color: const Color(0xFF1E293B),
          margin: const EdgeInsets.only(bottom: 12),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
          child: ListTile(
            contentPadding: const EdgeInsets.all(12),
            leading: ClipRRect(
              borderRadius: BorderRadius.circular(10),
              child: Image.network(
                curso['image'], 
                width: 60, height: 60, fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) => const Icon(Icons.book, size: 40),
              ),
            ),
            title: Text(curso['title'], style: const TextStyle(fontWeight: FontWeight.bold)),
            subtitle: Text(isPurchased ? "✅ Acceso concedido" : "🔒 Contenido bloqueado"),
            trailing: Icon(
              isPurchased ? Icons.play_circle_fill : Icons.lock_outline,
              color: isPurchased ? Colors.green : Colors.blueAccent,
              size: 30,
            ),
          ),
        );
      },
    );
  }
}
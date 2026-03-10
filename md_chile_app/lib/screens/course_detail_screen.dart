import 'package:flutter/material.dart';

class CourseDetailScreen extends StatelessWidget {
  final Map curso;

  const CourseDetailScreen({super.key, required this.curso});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(curso['title']),
        backgroundColor: const Color(0xFF0055FF),
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Imagen del curso
            Container(
              height: 200,
              width: double.infinity,
              color: Colors.grey[300],
              child: const Icon(Icons.play_circle_fill, size: 80, color: Colors.white),
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "Contenido del Curso",
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    curso['description'] ?? "Sin descripción disponible.",
                    style: const TextStyle(fontSize: 16),
                  ),
                  const Divider(height: 30),
                  // Lista de lecciones (Simulada por ahora)
                  const ListTile(
                    leading: Icon(Icons.check_circle, color: Colors.green),
                    title: Text("Lección 1: Introducción"),
                    trailing: Icon(Icons.play_arrow),
                  ),
                  const ListTile(
                    leading: Icon(Icons.radio_button_unchecked),
                    title: Text("Lección 2: Estrategias Avanzadas"),
                    trailing: Icon(Icons.lock),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
import 'package:flutter/material.dart';
import 'package:youtube_player_flutter/youtube_player_flutter.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class CourseDetailScreen extends StatefulWidget {
  final dynamic curso;
  const CourseDetailScreen({super.key, required this.curso});

  @override
  State<CourseDetailScreen> createState() => _CourseDetailScreenState();
}

class _CourseDetailScreenState extends State<CourseDetailScreen> {
  List lecciones = [];
  bool cargando = true;
  YoutubePlayerController? _controller;
  int? leccionSeleccionadaId;

  @override
  void initState() {
    super.initState();
    obtenerLecciones();
  }

  Future<void> obtenerLecciones() async {
    final url = Uri.parse('http://127.0.0.1:8000/api/cursos/${widget.curso['id']}/lecciones/');
    try {
      final respuesta = await http.get(url);
      if (respuesta.statusCode == 200) {
        setState(() {
          lecciones = json.decode(respuesta.body);
          cargando = false;
        });
      }
    } catch (e) {
      setState(() => cargando = false);
    }
  }

  // Sensor de telemetría: Envía el progreso a Django
  Future<void> marcarCompletada(int lessonId) async {
    final url = Uri.parse('http://127.0.0.1:8000/api/lecciones/$lessonId/completar/');
    try {
      final respuesta = await http.post(url);
      if (respuesta.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("¡Misión cumplida! Progreso guardado en la nube.")),
        );
      }
    } catch (e) {
      debugPrint("Fallo en el enlace de telemetría: $e");
    }
  }

  void _reproducirVideo(dynamic leccion) {
    String? videoId = YoutubePlayer.convertUrlToId(leccion['video_url']);
    if (videoId != null) {
      setState(() {
        leccionSeleccionadaId = leccion['id'];
        if (_controller != null) {
          _controller!.load(videoId);
        } else {
          _controller = YoutubePlayerController(
            initialVideoId: videoId,
            flags: const YoutubePlayerFlags(autoPlay: true, mute: false),
          );
        }
      });
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.curso['title'])),
      body: Column(
        children: [
          // Pantalla de video o imagen de curso
          _controller != null
              ? YoutubePlayer(controller: _controller!, showVideoProgressIndicator: true)
              : Image.network(widget.curso['image'], width: double.infinity, height: 200, fit: BoxFit.cover),
          
          if (leccionSeleccionadaId != null)
            Padding(
              padding: const EdgeInsets.all(12.0),
              child: ElevatedButton.icon(
                onPressed: () => marcarCompletada(leccionSeleccionadaId!),
                icon: const Icon(Icons.check_circle),
                label: const Text("COMPLETAR ESTA CLASE"),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green, 
                  foregroundColor: Colors.white,
                  minimumSize: const Size(double.infinity, 50)
                ),
              ),
            ),

          Expanded(
            child: ListView.builder(
              itemCount: lecciones.length,
              itemBuilder: (context, index) {
                return ListTile(
                  leading: const Icon(Icons.play_circle_fill, color: Colors.red),
                  title: Text(lecciones[index]['title']),
                  onTap: () => _reproducirVideo(lecciones[index]),
                );
              },
            ),
          ),
        ],
      ),
        );
  }
}
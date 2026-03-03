import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:youtube_player_flutter/youtube_player_flutter.dart'; 

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Academia MD Chile',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0055FF)),
      ),
      home: const DashboardCursos(),
    );
  }
}

class DashboardCursos extends StatefulWidget {
  const DashboardCursos({super.key});
  @override
  State<DashboardCursos> createState() => _DashboardCursosState();
}

class _DashboardCursosState extends State<DashboardCursos> {
  List cursos = [];
  bool cargando = true;

  @override
  void initState() {
    super.initState();
    obtenerCursos();
  }

  Future<void> obtenerCursos() async {
    final url = Uri.parse('http://127.0.0.1:8000/api/cursos/');
    try {
      final respuesta = await http.get(url);
      if (respuesta.statusCode == 200) {
        setState(() {
          cursos = json.decode(respuesta.body);
          cargando = false;
        });
      }
    } catch (e) {
      debugPrint("Fallo de red: $e");
      setState(() => cargando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF0055FF),
        title: const Text('MD Chile - Mis Cursos', style: TextStyle(color: Colors.white)),
        centerTitle: true,
      ),
      body: cargando 
        ? const Center(child: CircularProgressIndicator()) 
        : ListView.builder(
            itemCount: cursos.length,
            itemBuilder: (context, index) {
              final curso = cursos[index];
              return Card(
                margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: ListTile(
                  leading: ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: curso['image'] != null 
                      ? Image.network(curso['image'], width: 50, height: 50, fit: BoxFit.cover)
                      : const Icon(Icons.school),
                  ),
                  title: Text(curso['title'], style: const TextStyle(fontWeight: FontWeight.bold)),
                  trailing: const Icon(Icons.arrow_forward_ios, size: 14),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => DetalleCursoScreen(curso: curso)),
                    );
                  },
                ),
              );
            },
          ),
    );
  }
}

class DetalleCursoScreen extends StatefulWidget {
  final dynamic curso;
  const DetalleCursoScreen({super.key, required this.curso});
  @override
  State<DetalleCursoScreen> createState() => _DetalleCursoScreenState();
}

class _DetalleCursoScreenState extends State<DetalleCursoScreen> {
  List lecciones = [];
  bool cargandoLecciones = true;
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
          cargandoLecciones = false;
        });
      }
    } catch (e) {
      setState(() => cargandoLecciones = false);
    }
  }

  Future<void> marcarCompletada(int lessonId) async {
    final url = Uri.parse('http://127.0.0.1:8000/api/lecciones/$lessonId/completar/');
    try {
      final respuesta = await http.post(url);
      if (respuesta.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Progreso actualizado en la nube de MD Chile")),
        );
      }
    } catch (e) {
      debugPrint("Error de telemetría: $e");
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
          _controller != null
              ? YoutubePlayer(controller: _controller!, showVideoProgressIndicator: true)
              : widget.curso['image'] != null 
                  ? Image.network(widget.curso['image'], width: double.infinity, height: 220, fit: BoxFit.cover)
                  : Container(height: 220, color: Colors.blueGrey),
          
          if (leccionSeleccionadaId != null)
            Padding(
              padding: const EdgeInsets.all(12.0),
              child: ElevatedButton.icon(
                onPressed: () => marcarCompletada(leccionSeleccionadaId!),
                icon: const Icon(Icons.check_circle),
                label: const Text("MARCAR LECCIÓN COMO VISTA"),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green, 
                  foregroundColor: Colors.white,
                  minimumSize: const Size(double.infinity, 50)
                ),
              ),
            ),

          Expanded(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text("Clases Disponibles", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  const Divider(),
                  cargandoLecciones 
                    ? const Center(child: CircularProgressIndicator())
                    : Expanded(
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
            ),
          ),
        ],
      ),
    );
  }
}
import 'package:flutter/material.dart';
import '../services/api_service.dart'; // Importamos el sensor
import 'course_detail_screen.dart'; 
import 'store_screen.dart'; // IMPORTADO: Nueva pantalla de tienda

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  List cursos = [];
  bool cargando = true;

  @override
  void initState() {
    super.initState();
    cargarDatos();
  }

  void cargarDatos() async {
    final datos = await ApiService.obtenerCursos();
    setState(() {
      cursos = datos;
      cargando = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("MD Chile - Mis Cursos"),
        backgroundColor: const Color(0xFF0055FF),
        foregroundColor: Colors.white,
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const UserAccountsDrawerHeader(
              decoration: BoxDecoration(color: Color(0xFF0055FF)),
              accountName: Text("Capitán Angelo", style: TextStyle(fontWeight: FontWeight.bold)),
              accountEmail: Text("angelo@mdchile.cl"),
              currentAccountPicture: CircleAvatar(
                backgroundColor: Colors.white,
                child: Icon(Icons.person, size: 45, color: Color(0xFF0055FF)),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.school, color: Color(0xFF0055FF)),
              title: const Text("Mis Cursos Activos"),
              onTap: () => Navigator.pop(context),
            ),
            // ACTUALIZACIÓN: Botón funcional hacia la Tienda
            ListTile(
              leading: const Icon(Icons.store, color: Color(0xFF0055FF)),
              title: const Text("Tienda de Cursos"),
              onTap: () {
                Navigator.pop(context); // Cierra el menú
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const StoreScreen()),
                );
              },
            ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.logout, color: Colors.red),
              title: const Text("Cerrar Sesión"),
              onTap: () => Navigator.pushReplacementNamed(context, '/'),
            ),
          ],
        ),
      ),
      body: cargando 
        ? const Center(child: CircularProgressIndicator())
        : ListView.builder(
            padding: const EdgeInsets.all(10),
            itemCount: cursos.length,
            itemBuilder: (context, index) {
              final curso = cursos[index];
              return Card(
                elevation: 4,
                margin: const EdgeInsets.symmetric(vertical: 8),
                child: ListTile(
                  leading: curso['image'] != null 
                    ? Image.network(curso['image'], width: 60, height: 60, fit: BoxFit.cover)
                    : const Icon(Icons.book, size: 50),
                  title: Text(curso['title'], style: const TextStyle(fontWeight: FontWeight.bold)),
                  trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => CourseDetailScreen(curso: curso),
                      ),
                    );
                  },
                ),
              );
            },
          ),
    );
  }
}
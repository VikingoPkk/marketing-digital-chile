import 'package:flutter/material.dart';
import '../services/api_service.dart'; // Sensor actualizado
import 'course_detail_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  List cursos = [];
  bool cargando = true;
  bool mostrarTienda = false; // El interruptor táctico

  @override
  void initState() {
    super.initState();
    cargarDatos();
  }

  // Ahora el método es inteligente y sabe qué lista pedir
  void cargarDatos() async {
    setState(() => cargando = true);
    final datos = mostrarTienda 
        ? await ApiService.obtenerCursosTienda() 
        : await ApiService.obtenerCursosPropios();
    
    setState(() {
      cursos = datos;
      cargando = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(mostrarTienda ? "Tienda de Cursos" : "MD Chile - Mis Cursos"),
        backgroundColor: mostrarTienda ? Colors.orange : const Color(0xFF0055FF), // Cambio visual
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const UserAccountsDrawerHeader(
              decoration: BoxDecoration(color: Color(0xFF0055FF)),
              accountName: Text("Usuario Stark", style: TextStyle(fontWeight: FontWeight.bold)),
              accountEmail: Text("stark@mdchile.cl"),
              currentAccountPicture: CircleAvatar(backgroundColor: Colors.white, child: Icon(Icons.person)),
            ),
            // BOTÓN 1: MIS CURSOS
            ListTile(
              leading: const Icon(Icons.school, color: Color(0xFF0055FF)),
              title: const Text("Mis Cursos Activos"),
              selected: !mostrarTienda,
              onTap: () {
                setState(() => mostrarTienda = false);
                Navigator.pop(context);
                cargarDatos();
              },
            ),
            // BOTÓN 2: TIENDA
            ListTile(
              leading: const Icon(Icons.store, color: Colors.orange),
              title: const Text("Tienda de Cursos"),
              selected: mostrarTienda,
              onTap: () {
                setState(() => mostrarTienda = true);
                Navigator.pop(context);
                cargarDatos();
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
        : RefreshIndicator(
            onRefresh: () async => cargarDatos(),
            child: ListView.builder(
              padding: const EdgeInsets.all(10),
              itemCount: cursos.length,
              itemBuilder: (context, index) {
                final curso = cursos[index];
                return Card(
                  elevation: 4,
                  margin: const EdgeInsets.symmetric(vertical: 8),
                  child: ListTile(
                    leading: const Icon(Icons.book, size: 50),
                    title: Text(curso['title'], style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: mostrarTienda ? Text("Precio: ${curso['price'] ?? 'Consultar'}") : null,
                    trailing: Icon(mostrarTienda ? Icons.add_shopping_cart : Icons.arrow_forward_ios),
                    onTap: () {
                      // Si está en la tienda, podríamos llevarlo al checkout
                      if (!mostrarTienda) {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => CourseDetailScreen(curso: curso)),
                        );
                      }
                    },
                  ),
                );
              },
            ),
          ),
    );
  }
}
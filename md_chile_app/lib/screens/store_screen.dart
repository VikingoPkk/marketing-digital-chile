import 'package:flutter/material.dart';
import '../services/api_service.dart';

class StoreScreen extends StatefulWidget {
  const StoreScreen({super.key});

  @override
  State<StoreScreen> createState() => _StoreScreenState();
}

class _StoreScreenState extends State<StoreScreen> {
  List cursosDisponibles = [];
  bool cargando = true;

  @override
  void initState() {
    super.initState();
    cargarCursosTienda();
  }

  // Sensor: Filtra cursos que no están en la lista de "Mis Cursos"
  void cargarCursosTienda() async {
    final todosLosCursos = await ApiService.obtenerCursos();
    setState(() {
      cursosDisponibles = todosLosCursos; // Aquí aplicaremos el filtro de compra luego
      cargando = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Tienda MD Chile"),
        backgroundColor: Colors.orangeAccent,
      ),
      body: cargando 
        ? const Center(child: CircularProgressIndicator())
        : ListView.builder(
            padding: const EdgeInsets.all(15),
            itemCount: cursosDisponibles.length,
            itemBuilder: (context, index) {
              final curso = cursosDisponibles[index];
              return Card(
                child: Column(
                  children: [
                    Image.network(curso['image'], height: 150, width: double.infinity, fit: BoxFit.cover),
                    ListTile(
                      title: Text(curso['title'], style: const TextStyle(fontWeight: FontWeight.bold)),
                      subtitle: const Text("Disponible ahora"),
                      trailing: ElevatedButton(
                        onPressed: () {
                          // Aquí inyectaremos el WebView de pago luego
                        },
                        child: const Text("COMPRAR"),
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
    );
  }
}
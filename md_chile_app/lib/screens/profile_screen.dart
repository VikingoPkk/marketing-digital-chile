import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_service.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0B1220),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white), 
          onPressed: () => Navigator.pop(context)
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout, color: Colors.red),
            onPressed: () async {
              final prefs = await SharedPreferences.getInstance();
              await prefs.remove('auth_token');
              Navigator.pushReplacementNamed(context, '/login');
            },
          ),
        ],
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: ApiService.obtenerPerfilUsuario(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError || !snapshot.hasData) {
            return const Center(child: Text("Error al cargar perfil", style: TextStyle(color: Colors.white)));
          }

          final datos = snapshot.data!;
          
          // Lógica de materialización de nombre Angelo Wilche H
          final nombreCompleto = "${datos['first_name'] ?? ''} ${datos['last_name'] ?? ''}".trim();
          final nombreFinal = nombreCompleto.isNotEmpty ? nombreCompleto : "Angelo Wilche H";
          final urlFoto = datos['foto_url']; // Usamos el nuevo campo de Django

          return Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20),
            child: Column(
              children: [
                // Cabecera con Foto Real
                CircleAvatar(
                  radius: 45,
                  backgroundColor: Colors.blue,
                  backgroundImage: urlFoto != null ? NetworkImage(urlFoto) : null,
                  child: urlFoto == null 
                    ? const Icon(Icons.person, size: 45, color: Colors.white) 
                    : null,
                ),
                const SizedBox(height: 15),
                Text(
                  "¡Hola, $nombreFinal!",
                  style: const TextStyle(
                    color: Colors.white, 
                    fontSize: 22, 
                    fontWeight: FontWeight.bold
                  ),
                ),
                const Text(
                  "Chile", 
                  style: TextStyle(color: Colors.grey, fontSize: 16)
                ),
                const SizedBox(height: 30),
                
                // Tarjeta de Puntos
                Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: const Color(0xFF1A2235), 
                    borderRadius: BorderRadius.circular(20)
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      _buildStatColumn("Posición Semanal", "#789", Colors.blue),
                      _buildStatColumn("Puntos Totales", "1.250 pts", Colors.blue),
                    ],
                  ),
                ),
                const SizedBox(height: 40),
                
                // Sección de Certificados
                ListTile(
                  leading: const Icon(Icons.emoji_events, color: Colors.amber, size: 30),
                  title: const Text(
                    "Certificados Logrados", 
                    style: TextStyle(color: Colors.white, fontSize: 18)
                  ),
                  trailing: const Icon(Icons.arrow_forward_ios, color: Colors.grey, size: 18),
                  onTap: () {
                    // Acción para ver certificados
                  },
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildStatColumn(String label, String value, Color color) {
    return Column(children: [
      Text(label, style: const TextStyle(color: Colors.grey, fontSize: 14)),
      const SizedBox(height: 5),
      Text(value, style: TextStyle(color: color, fontSize: 20, fontWeight: FontWeight.bold)),
    ]);
  }
}
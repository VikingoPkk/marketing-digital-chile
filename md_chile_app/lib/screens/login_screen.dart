import 'package:flutter/material.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF0055FF), Color(0xFF0033AA)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Icono de cohete que representa el despegue de la academia
            const Icon(Icons.rocket_launch, size: 100, color: Colors.white),
            const SizedBox(height: 20),
            const Text(
              "¡Bienvenido a\nMarketing Digital Chile!",
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Colors.white,
                fontSize: 28,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 40),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 15),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(30),
                ),
              ),
              // ACTUALIZACIÓN: Navegación por nombre de ruta
              onPressed: () {
                Navigator.pushReplacementNamed(context, '/dashboard');
              },
              child: const Text(
                "INGRESAR A MIS CURSOS",
                style: TextStyle(fontSize: 16, color: Color(0xFF0055FF)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
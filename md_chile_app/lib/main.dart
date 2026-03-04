import 'package:flutter/material.dart';
// Importaciones relativas para evitar errores de nombre de paquete
import 'screens/login_screen.dart';
import 'screens/dashboard_screen.dart'; 

void main() => runApp(const AcademiaApp());

class AcademiaApp extends StatelessWidget {
  const AcademiaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Academia MD Chile',
      initialRoute: '/',
      routes: {
        // Sin const y con referencias directas a las clases importadas
        '/': (context) => LoginScreen(), 
        '/dashboard': (context) => DashboardScreen(),
      },
    );
  }
}
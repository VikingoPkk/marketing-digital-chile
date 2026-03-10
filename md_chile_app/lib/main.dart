import 'package:flutter/material.dart';
import 'services/auth_service.dart';
import 'screens/courses_screen.dart';

void main() => runApp(const MDChileApp());

class MDChileApp extends StatelessWidget {
  const MDChileApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'MD Chile Academy',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0F172A),
        primaryColor: const Color(0xFF2563EB),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: const Color(0xFF1E293B),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide.none,
          ),
        ),
      ),
      home: const MainNavigation(),
    );
  }
}

class MainNavigation extends StatefulWidget {
  const MainNavigation({super.key});

  @override
  State<MainNavigation> createState() => _MainNavigationState();
}

class _MainNavigationState extends State<MainNavigation> {
  int _selectedIndex = 4;

  void _onLoginSuccess() {
    setState(() {
      _selectedIndex = 2; 
    });
  }

  @override
  Widget build(BuildContext context) {
    final List<Widget> _pages = [
      const Center(child: Text("Inicio", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold))),
      const Center(child: Text("Buscar", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold))),
      const CoursesScreen(), 
      const Center(child: Text("Descargas", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold))),
      AuthService.accessToken == null 
          ? LoginTab(onLoginSuccess: _onLoginSuccess)
          : UserDashboard(onLogout: () {
              setState(() {
                AuthService.logout();
                _selectedIndex = 4;
              });
            }),
    ];

    return Scaffold(
      body: IndexedStack(index: _selectedIndex, children: _pages),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
        type: BottomNavigationBarType.fixed,
        selectedItemColor: const Color(0xFF2563EB),
        backgroundColor: const Color(0xFF1E293B),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home_filled), label: "Inicio"),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: "Buscar"),
          BottomNavigationBarItem(icon: Icon(Icons.layers), label: "Mis cursos"),
          BottomNavigationBarItem(icon: Icon(Icons.download), label: "Descargas"),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: "Mi perfil"),
        ],
      ),
    );
  }
}

class UserDashboard extends StatelessWidget {
  final VoidCallback onLogout;
  const UserDashboard({super.key, required this.onLogout});

  @override
  Widget build(BuildContext context) {
    final user = AuthService.userData; 

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        children: [
          const SizedBox(height: 50),
          Row(
            children: [
              CircleAvatar(
                radius: 35,
                backgroundColor: Colors.blue,
                backgroundImage: (user != null && user['profile_picture'] != null)
                  ? NetworkImage(user['profile_picture'])
                  : null,
                child: (user == null || user['profile_picture'] == null) 
                  ? const Icon(Icons.person, size: 40, color: Colors.white) 
                  : null,
              ),
              const SizedBox(width: 15),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    user?['full_name'] ?? "Usuario", 
                    style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)
                  ),
                  const Text("🇨🇱 Chile", style: TextStyle(color: Colors.white60)),
                ],
              ),
              const Spacer(),
              IconButton(
                onPressed: onLogout, 
                icon: const Icon(Icons.logout, color: Colors.redAccent)
              ),
            ],
          ),
          const SizedBox(height: 30),
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: const Color(0xFF1E293B), 
              borderRadius: BorderRadius.circular(20)
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _statItem("Posición Semanal", "#${user?['rank'] ?? '---'}"),
                const VerticalDivider(color: Colors.white24),
                _statItem("Puntos Totales", "${user?['points'] ?? '0'} pts"),
              ],
            ),
          ),
          const SizedBox(height: 30),
          const ListTile(
            leading: Icon(Icons.emoji_events, color: Colors.amber),
            title: Text("Certificados Logrados"),
            trailing: Icon(Icons.arrow_forward_ios, size: 14),
          ),
        ],
      ),
    );
  }

  Widget _statItem(String label, String value) {
    return Column(
      children: [
        Text(label, style: const TextStyle(fontSize: 12, color: Colors.white60)),
        Text(value, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.blue)),
      ],
    );
  }
}

class LoginTab extends StatefulWidget {
  final VoidCallback onLoginSuccess;
  const LoginTab({super.key, required this.onLoginSuccess});
  @override
  State<LoginTab> createState() => _LoginTabState();
}

class _LoginTabState extends State<LoginTab> {
  final _email = TextEditingController();
  final _pass = TextEditingController();
  bool _isLoading = false; 

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const SizedBox(height: 100),
          const Text("MD CHILE", style: TextStyle(fontSize: 28, fontWeight: FontWeight.w900, fontStyle: FontStyle.italic)),
          const SizedBox(height: 40),
          TextField(controller: _email, decoration: const InputDecoration(labelText: "Email")),
          const SizedBox(height: 16),
          TextField(controller: _pass, obscureText: true, decoration: const InputDecoration(labelText: "Password")),
          const SizedBox(height: 32),
          _isLoading 
            ? const CircularProgressIndicator()
            : ElevatedButton(
                onPressed: () async {
                  setState(() => _isLoading = true);
                  bool success = await AuthService().login(_email.text, _pass.text);
                  setState(() => _isLoading = false);
                  if (success) widget.onLoginSuccess();
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF2563EB), 
                  minimumSize: const Size(double.infinity, 55)
                ),
                child: const Text("INGRESAR"),
              ),
        ],
      ),
    );
  }
}
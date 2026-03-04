import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class CheckoutScreen extends StatefulWidget {
  final String urlPago; // URL generada por el backend Django
  const CheckoutScreen({super.key, required this.urlPago});

  @override
  State<CheckoutScreen> createState() => _CheckoutScreenState();
}

class _CheckoutScreenState extends State<CheckoutScreen> {
  late final WebViewController controller;

  @override
  void initState() {
    super.initState();
    controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageFinished: (String url) {
            // Si la URL contiene "success", la transacción fue exitosa
            if (url.contains('success')) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text("¡Pago Procesado! Bienvenido al curso.")),
              );
              Navigator.pop(context);
            }
          },
        ),
      )
      ..loadRequest(Uri.parse(widget.urlPago));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Pago Seguro MD Chile")),
      body: WebViewWidget(controller: controller),
    );
  }
}
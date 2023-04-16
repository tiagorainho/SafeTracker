import 'package:flutter/material.dart';
import 'homepage.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tracker',
      home: const Map(),
      theme: ThemeData(
      primarySwatch: Colors.lightBlue,
      scaffoldBackgroundColor: const Color(0xFF222222), //<-- SEE HERE
    ),
    );
  }
}
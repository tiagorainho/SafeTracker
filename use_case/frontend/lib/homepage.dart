import 'package:flutter/material.dart';
import 'package:google_nav_bar/google_nav_bar.dart';

import 'pages/search.dart';
import 'pages/map.dart';
import 'pages/account.dart';

class Map extends StatefulWidget {
  const Map({Key? key}) : super(key: key);

  @override
  State<Map> createState() => _MapState();
}

class _MapState extends State<Map> {

  int _selectedIndex = 1;

  void _navigateBottomBar(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  final List<Widget> _pages = [
    PageSearch(),
    PageMap(),
    PageAccount(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_selectedIndex],
      bottomNavigationBar: GNav( //https://www.youtube.com/watch?v=FEvYl8Mzsxw&ab_channel=MitchKoko TODO increase horiz padding
        backgroundColor: const Color(0xFF222222),
        color: Colors.grey,
        activeColor: const Color(0xFFD0BCFF),
        gap: 8,
        onTabChange: _navigateBottomBar,
        tabs: const [
          GButton(
            icon: Icons.search,
          ),
          GButton(icon: Icons.location_on),
          GButton(icon: Icons.person),
        ],
      ),
    );
  }
}

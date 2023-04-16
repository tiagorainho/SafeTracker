/* import 'package:flutter/material.dart';

class PageMap extends StatelessWidget {
  const PageMap({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text(
        'Map',
        style: TextStyle(
          color: Colors.white
        ),
      ),
    );
  }
} */

import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';


class PageMap extends StatelessWidget {
  final MapController mapController = MapController();
  final LatLng initialLocation = LatLng(40.2050, -8.4020);

  var marker = [
    Marker(
      point: LatLng(40.2055, -8.4020),
      builder: (ctx) => const Icon(Icons.account_circle,
      color: Color.fromARGB(255, 255, 3, 3),
       size: 40.0
      ),
    ),
    Marker(
      point: LatLng(40.2050, -8.4020),
      builder: (ctx) => const Icon(Icons.pin_drop_sharp),
    ),
    Marker(
      point: LatLng(40.2060, -8.4020),
      builder: (ctx) => const Icon(
        Icons.pin_end,
        color: Color.fromARGB(255, 255, 0, 0),
      ),
    ),
  ];

  PageMap({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
          child: Container(
              child: Column(
        children: [
          Flexible(
              child: FlutterMap(
                  options: MapOptions(center: initialLocation, zoom: 18),
                  layers: [
                TileLayerOptions(
                  urlTemplate:
                      'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                  subdomains: ['a', 'b', 'c'],
                ),
                MarkerLayerOptions(markers: marker)
              ]))
        ],
      ))),
    );
  }
}

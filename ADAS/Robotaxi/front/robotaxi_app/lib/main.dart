import 'package:flutter/material.dart';
import 'dart:math';
import 'dart:convert';
import 'dart:io';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: RobotaxiPrettyMap(),
    );
  }
}

class RobotaxiPrettyMap extends StatefulWidget {
  const RobotaxiPrettyMap({super.key});

  @override
  State<RobotaxiPrettyMap> createState() => _RobotaxiPrettyMapState();
}

class _RobotaxiPrettyMapState extends State<RobotaxiPrettyMap> {
  // Grid layout (19 rows, 15 columns)
  final List<List<int>> mapGrid = [
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 5, 1, 1, 1, 5, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 0],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 0, 0, 5, 1, 0, 0, 5, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
    [1, 5, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 5, 1, 1, 5, 0],
    [1, 1, 1, 0, 0, 5, 1, 0, 2, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 2, 0, 0, 2, 0, 2, 0, 0, 1],
  ];

  bool showDebugArUcos = false;
  double carSizeMultiplier = 1.3;
  Offset carGlobalOffset = const Offset(0.0, 0.0);

  // BASE LOCATIONS FOR ALL 16 ARUCOS (Col, Row)
  final Map<int, Offset> allArucoLocations = {
    0: const Offset(11, 14.5),   // 42 Porto
    1: const Offset(12, 11),     // Sea:Me
    2: const Offset(11, 6.5),    // Intersection
    3: const Offset(12, 4),      // Gelato
    4: const Offset(9, 2),       // Padle
    5: const Offset(7, 2),       // Upper Track
    6: const Offset(4.5, 2),     // Climbing
    7: const Offset(2, 4),       // Bank
    8: const Offset(4.2, 9),     // Grupo Brisa
    9: const Offset(2, 13),      // Hospital
    10: const Offset(3.5, 15.2), // Track
    11: const Offset(5.5, 16),   // Track
    12: const Offset(7.5, 15.8), // Track
    13: const Offset(10, 15.8),  // Track
    14: const Offset(8, 14.5),   // Track
    15: const Offset(7.5, 8),   // Parking / Start Position (Bottom)
  };

  // FINE-TUNE OFFSETS FOR ARUCOS (fractions of a cell)
  final Map<int, Offset> arucoCustomOffsets = {
    0: const Offset(0.0, 0.0),    // 42 Porto
    1: const Offset(-0.95, -0.9), // Sea:Me
    2: const Offset(0.0, 0.0),    // Intersection
    3: const Offset(-0.95, 0.0),  // Gelato
    4: const Offset(0.6, 0.2),    // Padle
    5: const Offset(-0.2, 0.2),   // Upper Track
    6: const Offset(-0.8, 0.2),   // Climbing
    7: const Offset(0.2, 0.0),    // Bank
    8: const Offset(0.0, 0.0),    // Grupo Brisa
    9: const Offset(0.8, 0.0),    // Hospital
    10: const Offset(0.0, 0.0),   // Track
    11: const Offset(0.0, 0.0),   // Track
    12: const Offset(0.0, 0.0),   // Track
    13: const Offset(0.0, 0.0),   // Track
    14: const Offset(-0.5, 0.0),  // Track
    15: const Offset(0.0, 0.0),   // Parking Spot
  };

  // BUILDING DATA
  final Map<Offset, String> buildingNames = {
    const Offset(5, 1): "Climbing",
    const Offset(9, 1): "Padle",
    const Offset(1, 4): "Bank",
    const Offset(13, 4): "Gelato",
    const Offset(2, 9): "Grupo Brisa",
    const Offset(13, 9): "Sea:Me",
    const Offset(13, 14): "42 Porto",
    const Offset(1, 13): "Hospital",
  };

  final Map<Offset, String> buildingAssets = {
    const Offset(5, 1): "assets/climbing.png",
    const Offset(9, 1): "assets/padle.png",
    const Offset(1, 4): "assets/bank.png",
    const Offset(13, 4): "assets/gelado.png",
    const Offset(2, 9): "assets/brisa.png",
    const Offset(13, 9): "assets/seame.png",
    const Offset(13, 14): "assets/42porto.png",
    const Offset(1, 13): "assets/hospital.png",
  };

  final Map<Offset, Offset> buildingCustomOffsets = {
    const Offset(5, 1): const Offset(-0.5, -0.5),
    const Offset(9, 1): const Offset(0.3, -0.3),
    const Offset(1, 4): const Offset(-0.5, -0.2),
    const Offset(13, 4): const Offset(0.0, 0.0),
    const Offset(2, 9): const Offset(-0.6, -0.2),
    const Offset(13, 9): const Offset(0.0, 0.0),
    const Offset(13, 14): const Offset(0.2, -1),
    const Offset(1, 13): const Offset(0.0, 0.0),
  };

  final Map<Offset, double> buildingSizes = {
    const Offset(5, 1): 2.8,
    const Offset(9, 1): 4.2,
    const Offset(1, 4): 2.8,
    const Offset(13, 4): 2.8,
    const Offset(2, 9): 3.3,
    const Offset(13, 9): 3.0,
    const Offset(13, 14): 3.2,
    const Offset(1, 13): 2.8,
  };

  final Map<Offset, int> buildingArucoIds = {
    const Offset(5, 1): 6,
    const Offset(9, 1): 4,
    const Offset(1, 4): 7,
    const Offset(13, 4): 3,
    const Offset(2, 9): 8,
    const Offset(13, 9): 1,
    const Offset(13, 14): 0,
    const Offset(1, 13): 9,
  };

  Offset? pickupPoint;
  Offset? dropoffPoint;
  
  // STATE VARIABLES
  // Car explicitly starts at ArUco 15 Parking Spot
  late Offset carPosition;
  double carAngle = 0.0; 
  Offset? _lastCarPosition;
  
  int activeCarArucoId = 15;
  int lastDetectedArucoId = 15;
  double lastDetectedDistanceCm = 999.0;

  // NETWORK SETTINGS
  String serverIp = "10.21.100.5:8000";
  WebSocket? _webSocket;
  bool isConnected = false;
  String robotStatus = "Disconnected";
  String missionState = "Unknown";
  String lastArUcoDetected = "None";

  @override
  void initState() {
    super.initState();
    // Initialize car strictly at Parking (ArUco 15)
    carPosition = allArucoLocations[15]!;
    _connectWebSocket();
  }

  @override
  void dispose() {
    _webSocket?.close();
    super.dispose();
  }

  String _getSanitizedIp() {
    String clean = serverIp.trim();
    clean = clean.replaceAll(RegExp(r'^(https?://|ws://)'), '');
    if (clean.endsWith('/')) {
      clean = clean.substring(0, clean.length - 1);
    }
    if (clean.endsWith('/ws/frontend')) {
      clean = clean.replaceAll('/ws/frontend', '');
    }
    return clean;
  }

  Future<void> _connectWebSocket() async {
    _webSocket?.close();
    setState(() {
      isConnected = false;
      robotStatus = "Connecting...";
    });

    try {
      final cleanIp = _getSanitizedIp();
      final wsUrl = "ws://$cleanIp/ws/frontend";
      _webSocket = await WebSocket.connect(wsUrl).timeout(const Duration(seconds: 4));
      
      setState(() {
        isConnected = true;
        robotStatus = "Connected";
      });

      _webSocket!.listen(
        (data) {
          final decoded = jsonDecode(data);
          _handleWebSocketMessage(decoded);
        },
        onError: (err) => _handleDisconnect(),
        onDone: () => _handleDisconnect(),
      );
    } catch (e) {
      _handleDisconnect();
    }
  }

  void _handleDisconnect() {
    if (mounted) {
      setState(() {
        isConnected = false;
        robotStatus = "Disconnected";
        missionState = "Unknown";
      });
    }
  }

  void _handleWebSocketMessage(Map<String, dynamic> message) {
    if (message["type"] == "telemetry") {
      final telemetry = message["telemetry"];
      if (telemetry != null) {
        setState(() {
          missionState = telemetry["mission_state"] ?? "Inactive";
          
          final arucoData = telemetry["aruco"];
          if (arucoData != null && arucoData["id"] != null) {
            final int detectedId = (arucoData["id"] as num).toInt();
            final double distCm = (arucoData["distance_cm"] as num?)?.toDouble() ?? 999.0;

            lastDetectedArucoId = detectedId;
            lastDetectedDistanceCm = distCm;
            lastArUcoDetected = "ID $detectedId (${distCm.toStringAsFixed(1)} cm)";

            final pickupArucoId = pickupPoint != null ? buildingArucoIds[pickupPoint] : null;
            final dropoffArucoId = dropoffPoint != null ? buildingArucoIds[dropoffPoint] : null;

            // STRICT FILTERING: Car position ONLY updates if:
            // 1. ArUco 15 (Parking) is detected
            // 2. Pickup ArUco is detected AND distance <= 35cm
            // 3. Dropoff ArUco is detected AND distance <= 35cm
            bool shouldUpdateCarPos = false;

            if (detectedId == 15) {
              shouldUpdateCarPos = true;
            } else if (pickupArucoId != null && detectedId == pickupArucoId && distCm <= 35.0) {
              shouldUpdateCarPos = true;
            } else if (dropoffArucoId != null && detectedId == dropoffArucoId && distCm <= 35.0) {
              shouldUpdateCarPos = true;
            }

            if (shouldUpdateCarPos && allArucoLocations.containsKey(detectedId)) {
              activeCarArucoId = detectedId;
              Offset newPos = allArucoLocations[detectedId]!;
              
              if (_lastCarPosition != null && _lastCarPosition != newPos) {
                double dx = newPos.dx - _lastCarPosition!.dx;
                double dy = newPos.dy - _lastCarPosition!.dy;
                if (dx != 0 || dy != 0) {
                  carAngle = atan2(dy, dx);
                }
              }
              _lastCarPosition = carPosition;
              carPosition = newPos;
            }
          }
        });
      }
    }
  }

  Future<void> _sendStartMission() async {
    if (pickupPoint == null || dropoffPoint == null) return;

    final pickupId = buildingArucoIds[pickupPoint];
    final dropoffId = buildingArucoIds[dropoffPoint];

    if (pickupId == null || dropoffId == null) return;

    final payload = {
      "command": "start_mission",
      "pickup": pickupId,
      "dropoff": dropoffId,
    };
    final payloadJson = jsonEncode(payload);

    try {
      final cleanIp = _getSanitizedIp();
      final client = HttpClient();
      final uri = Uri.parse("http://$cleanIp/mission/command");
      final request = await client.postUrl(uri);
      
      request.headers.contentType = ContentType.json;
      request.write(payloadJson);

      final response = await request.close();
      if (!mounted) return;
      
      if (response.statusCode == 202) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text("Sent: $payloadJson"),
            backgroundColor: Colors.green,
            duration: const Duration(seconds: 4),
          ),
        );
      } else {
        throw Exception("${response.statusCode}");
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Failed to send ($payloadJson): $e"),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  void handleTap(TapUpDetails details, double cellSize) {
    double tappedCol = details.localPosition.dx / cellSize;
    double tappedRow = details.localPosition.dy / cellSize;

    double minDistance = double.infinity;
    Offset? closestBuilding;

    for (int r = 0; r < 19; r++) {
      for (int c = 0; c < 15; c++) {
        if (mapGrid[r][c] == 5) {
          double distance = sqrt(pow(tappedCol - c, 2) + pow(tappedRow - r, 2));
          if (distance < minDistance) {
            minDistance = distance;
            closestBuilding = Offset(c.toDouble(), r.toDouble());
          }
        }
      }
    }

    if (closestBuilding != null && minDistance <= 2.2) {
      setState(() {
        if (pickupPoint == null) {
          pickupPoint = closestBuilding;
        } else if (dropoffPoint == null) {
          if (closestBuilding != pickupPoint) {
            dropoffPoint = closestBuilding;
          }
        } else {
          pickupPoint = closestBuilding;
          dropoffPoint = null;
        }
      });
    }
  }

  String _getBuildingName(Offset? point) {
    if (point == null) return "Pending";
    return buildingNames[point] ?? "Building [${point.dx.toInt()},${point.dy.toInt()}]";
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    if (screenWidth > 500) screenWidth = 400; 
    
    double cellSize = (screenWidth - 32) / 15;
    double mapHeight = cellSize * 19;
    double mapWidth = cellSize * 15;

    double carWidth = cellSize * carSizeMultiplier;
    double carHeight = cellSize * carSizeMultiplier;

    Offset arucoOffset = arucoCustomOffsets[activeCarArucoId] ?? const Offset(0, 0);

    double effectiveCol = carPosition.dx + carGlobalOffset.dx + arucoOffset.dx;
    double effectiveRow = carPosition.dy + carGlobalOffset.dy + arucoOffset.dy;

    double carLeft = (effectiveCol * cellSize) - (carWidth - cellSize) / 2;
    double carTop = (effectiveRow * cellSize) - (carHeight - cellSize) / 2;

    return Scaffold(
      backgroundColor: const Color(0xFF121214),
      appBar: AppBar(
        title: const Text('Robotaxi Navigator', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.black26,
        centerTitle: true,
        actions: [
          IconButton(
            tooltip: "ArUco Calibration Mode",
            icon: Icon(Icons.bug_report, color: showDebugArUcos ? Colors.blueAccent : Colors.grey),
            onPressed: () => setState(() => showDebugArUcos = !showDebugArUcos),
          ),
          IconButton(
            tooltip: "IP Settings",
            icon: Icon(Icons.settings, color: isConnected ? Colors.greenAccent : Colors.redAccent),
            onPressed: () => _showSettingsDialog(),
          ),
        ],
      ),
      body: Center(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                _buildTelemetryPanel(),
                const SizedBox(height: 12),
                _buildStatusPanel(),
                const SizedBox(height: 12),
                
                GestureDetector(
                  onTapUp: (details) => handleTap(details, cellSize),
                  child: Container(
                    width: mapWidth,
                    height: mapHeight,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.white12),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withValues(alpha: 0.5),
                          blurRadius: 15,
                          offset: const Offset(0, 5),
                        ),
                      ],
                    ),
                    clipBehavior: Clip.hardEdge,
                    child: Stack(
                      children: [
                        // Layer 1: Background Map
                        Image.asset(
                          'assets/mapa.png',
                          width: mapWidth,
                          height: mapHeight,
                          fit: BoxFit.fill,
                        ),

                        // Layer 1.5: Debug Blue Boxes for ALL 16 ARUCOS
                        if (showDebugArUcos)
                          ...allArucoLocations.entries.map((entry) {
                            final int id = entry.key;
                            final Offset pos = entry.value;
                            final Offset offset = arucoCustomOffsets[id] ?? const Offset(0, 0);

                            final double effectiveCol = pos.dx + offset.dx;
                            final double effectiveRow = pos.dy + offset.dy;

                            final double boxLeft = effectiveCol * cellSize;
                            final double boxTop = effectiveRow * cellSize;

                            return Positioned(
                              left: boxLeft,
                              top: boxTop,
                              child: Container(
                                width: cellSize,
                                height: cellSize,
                                decoration: BoxDecoration(
                                  color: Colors.blue.withValues(alpha: 0.6),
                                  border: Border.all(color: Colors.white, width: 1.5),
                                  borderRadius: BorderRadius.circular(4),
                                ),
                                child: Center(
                                  child: Text(
                                    "ID $id",
                                    style: const TextStyle(
                                      color: Colors.white,
                                      fontSize: 9,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                              ),
                            );
                          }),

                        // Layer 2: Render selected buildings
                        ...buildingAssets.entries.map((entry) {
                          final Offset pos = entry.key;
                          final String assetPath = entry.value;

                          final bool isPickup = pickupPoint == pos;
                          final bool isDropoff = dropoffPoint == pos;
                          final bool isSelected = isPickup || isDropoff;

                          if (!isSelected) return const SizedBox.shrink();

                          final Offset customOffset = buildingCustomOffsets[pos] ?? const Offset(0, 0);
                          final double scaleMultiplier = buildingSizes[pos] ?? 2.2;

                          final double buildingWidth = cellSize * scaleMultiplier;
                          final double buildingHeight = cellSize * scaleMultiplier;

                          final double posX = ((pos.dx + customOffset.dx) * cellSize) - (buildingWidth - cellSize) / 2;
                          final double posY = ((pos.dy + customOffset.dy) * cellSize) - (buildingHeight - cellSize) / 2;

                          final Color accentColor = isPickup ? Colors.greenAccent : Colors.redAccent;
                          const double strokeOffset = 1.2;

                          return Positioned(
                            left: posX,
                            top: posY,
                            child: IgnorePointer(
                              child: AnimatedScale(
                                duration: const Duration(milliseconds: 300),
                                curve: Curves.easeOutBack,
                                scale: 1.3,
                                child: SizedBox(
                                  width: buildingWidth,
                                  height: buildingHeight,
                                  child: Stack(
                                    alignment: Alignment.center,
                                    children: [
                                      Container(
                                        width: buildingWidth * 0.65,
                                        height: buildingHeight * 0.65,
                                        decoration: BoxDecoration(
                                          shape: BoxShape.circle,
                                          boxShadow: [
                                            BoxShadow(
                                              color: accentColor.withValues(alpha: 0.5),
                                              blurRadius: 18,
                                              spreadRadius: 4,
                                            ),
                                            BoxShadow(
                                              color: Colors.black.withValues(alpha: 0.4),
                                              blurRadius: 8,
                                              spreadRadius: 2,
                                            ),
                                          ],
                                        ),
                                      ),
                                      for (double dx = -strokeOffset; dx <= strokeOffset; dx += strokeOffset)
                                        for (double dy = -strokeOffset; dy <= strokeOffset; dy += strokeOffset)
                                          if (dx != 0 || dy != 0)
                                            Positioned(
                                              left: dx,
                                              top: dy,
                                              child: ColorFiltered(
                                                colorFilter: ColorFilter.mode(accentColor, BlendMode.srcIn),
                                                child: Image.asset(
                                                  assetPath,
                                                  fit: BoxFit.contain,
                                                  width: buildingWidth,
                                                  height: buildingHeight,
                                                ),
                                              ),
                                            ),
                                      Image.asset(
                                        assetPath,
                                        fit: BoxFit.contain,
                                        width: buildingWidth,
                                        height: buildingHeight,
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                          );
                        }),

                        // Layer 3: Animated Car (Slides to Parking / Pickup / Dropoff)
                        AnimatedPositioned(
                          duration: const Duration(milliseconds: 1000),
                          curve: Curves.easeInOutBack,
                          left: carLeft,
                          top: carTop,
                          child: Transform.rotate(
                            angle: carAngle,
                            child: SizedBox(
                              width: carWidth,
                              height: carHeight,
                              child: Image.asset(
                                'assets/carro.png',
                                fit: BoxFit.contain,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 12),
                if (pickupPoint != null && dropoffPoint != null)
                  ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.greenAccent.withValues(alpha: 0.15),
                      foregroundColor: Colors.greenAccent,
                      side: const BorderSide(color: Colors.greenAccent, width: 1.5),
                      padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 24),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                    onPressed: _sendStartMission,
                    icon: const Icon(Icons.play_arrow),
                    label: const Text('Start', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  ),
                const SizedBox(height: 8),
                TextButton.icon(
                  onPressed: () {
                    setState(() {
                      pickupPoint = null;
                      dropoffPoint = null;
                      // Reset car position back to Parking (ArUco 15)
                      activeCarArucoId = 15;
                      lastDetectedArucoId = 15;
                      lastDetectedDistanceCm = 999.0;
                      carPosition = allArucoLocations[15]!;
                    });
                  },
                  icon: const Icon(Icons.refresh, color: Colors.grey),
                  label: const Text('Reset Selections', style: TextStyle(color: Colors.grey)),
                )
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTelemetryPanel() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.blueGrey.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: isConnected ? Colors.green.withValues(alpha: 0.2) : Colors.red.withValues(alpha: 0.2)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text("Backend Status: $robotStatus", style: TextStyle(color: isConnected ? Colors.greenAccent : Colors.redAccent, fontSize: 12, fontWeight: FontWeight.bold)),
              Icon(Icons.wifi, color: isConnected ? Colors.greenAccent : Colors.red, size: 16),
            ],
          ),
          const Divider(color: Colors.white10, height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text("Mission: $missionState", style: const TextStyle(color: Colors.white70, fontSize: 12)),
              Text("Last ArUco: $lastArUcoDetected", style: const TextStyle(color: Colors.white54, fontSize: 12)),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildStatusPanel() {
    // Arrival logic check: MUST match ArUco ID AND be <= 35cm distance
    final pickupArucoId = pickupPoint != null ? buildingArucoIds[pickupPoint] : null;
    final dropoffArucoId = dropoffPoint != null ? buildingArucoIds[dropoffPoint] : null;

    bool hasArrivedAtPickup = pickupArucoId != null &&
        lastDetectedArucoId == pickupArucoId &&
        lastDetectedDistanceCm <= 35.0;

    bool hasArrivedAtDropoff = dropoffArucoId != null &&
        lastDetectedArucoId == dropoffArucoId &&
        lastDetectedDistanceCm <= 35.0;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
      decoration: BoxDecoration(
        color: hasArrivedAtPickup 
            ? Colors.greenAccent.withValues(alpha: 0.15)
            : hasArrivedAtDropoff
                ? Colors.redAccent.withValues(alpha: 0.15)
                : Colors.white.withValues(alpha: 0.05),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: hasArrivedAtPickup 
              ? Colors.greenAccent.withValues(alpha: 0.5)
              : hasArrivedAtDropoff
                  ? Colors.redAccent.withValues(alpha: 0.5)
                  : Colors.white.withValues(alpha: 0.05),
        ),
      ),
      child: Column(
        children: [
          if (hasArrivedAtPickup)
            const Padding(
              padding: EdgeInsets.only(bottom: 8.0),
              child: Text("📍 ARRIVED AT PICKUP!", style: TextStyle(color: Colors.greenAccent, fontWeight: FontWeight.bold, fontSize: 16)),
            ),
          if (hasArrivedAtDropoff)
            const Padding(
              padding: EdgeInsets.only(bottom: 8.0),
              child: Text("🏁 ARRIVED AT DROPOFF!", style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold, fontSize: 16)),
            ),
            
          Row(
            children: [
              const Icon(Icons.location_on, color: Colors.greenAccent, size: 18),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  'Pickup: ${_getBuildingName(pickupPoint)}',
                  style: TextStyle(
                    color: pickupPoint != null ? Colors.greenAccent : Colors.white60, 
                    fontSize: 13,
                    fontWeight: pickupPoint != null ? FontWeight.bold : FontWeight.normal,
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
          const Divider(color: Colors.white10, height: 16),
          Row(
            children: [
              const Icon(Icons.flag, color: Colors.redAccent, size: 18),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  'Dropoff: ${_getBuildingName(dropoffPoint)}',
                  style: TextStyle(
                    color: dropoffPoint != null ? Colors.redAccent : Colors.white60, 
                    fontSize: 13,
                    fontWeight: dropoffPoint != null ? FontWeight.bold : FontWeight.normal,
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  void _showSettingsDialog() {
    final controller = TextEditingController(text: serverIp);
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          backgroundColor: const Color(0xFF1E1E24),
          title: const Text("IP Settings", style: TextStyle(color: Colors.white)),
          content: TextField(
            controller: controller,
            style: const TextStyle(color: Colors.white),
            decoration: const InputDecoration(
              labelText: "Server IP and Port (e.g., 10.21.100.5:8000)",
              labelStyle: TextStyle(color: Colors.white60),
              enabledBorder: UnderlineInputBorder(borderSide: BorderSide(color: Colors.white24)),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text("Cancel", style: TextStyle(color: Colors.grey)),
            ),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  serverIp = controller.text;
                });
                Navigator.pop(context);
                _connectWebSocket();
              },
              child: const Text("Save and Connect"),
            )
          ],
        );
      },
    );
  }
}
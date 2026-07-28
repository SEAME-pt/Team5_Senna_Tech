import 'package:flutter/material.dart';
import 'dart:math';
import 'dart:convert';
import 'dart:io';
import 'dart:async';

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
  final List<List<int>> mapGrid = [
   //0  1  2  3  4  5  6  7  8  9  10 11 12 13 14
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], // Linha 0
    [1, 0, 0, 0, 1, 5, 1, 1, 1, 5, 1, 1, 1, 0, 0], // Linha 1 (Climbing Col 5, Padle Col 9)
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], // Linha 2
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], // Linha 3
    [1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 0], // Linha 4 (Bank Col 1, Gelato Col 13)
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], // Linha 5
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], // Linha 6
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], // Linha 7
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0], // Linha 8
    [1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 0], // Linha 9 (Grupo Brisa Col 2)
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0], // Linha 10 (Sea:Me Col 13)
    [1, 1, 1, 1, 0, 0, 5, 1, 0, 0, 5, 1, 1, 1, 0], // Linha 11
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1], // Linha 12
    [1, 5, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0], // Linha 13
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 5, 1, 1, 5, 0], // Linha 14 (42 Porto Col 13)
    [1, 1, 1, 0, 0, 5, 1, 0, 2, 0, 1, 1, 1, 1, 0], // Linha 15 (Hospital Col 1)
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0], // Linha 16
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1], // Linha 17
    [1, 1, 1, 1, 1, 1, 2, 0, 0, 2, 0, 2, 0, 0, 1], // Linha 18
  ];

  bool showDebugArUcos = true;
  double carSizeMultiplier = 1.3;
  Offset carGlobalOffset = const Offset(0.0, 0.0);

  // Tamanho em cm de cada célula da grade (para converter distance_cm em células)
  double cmPerCell = 30.0; 

  // MAPEAMENTO DOS 16 ARUCOS NA PISTA (IDs 0 a 15)
  final Map<int, Offset> allArucoLocations = {
    0: const Offset(11, 14.5), // 42 Porto
    1: const Offset(12, 11),  // Sea:Me
    2: const Offset(11, 6.5),
    3: const Offset(12, 4),  // Gelato
    4: const Offset(9, 2),   // Padle
    5: const Offset(7, 2),
    6: const Offset(4.5, 2),   // Climbing
    7: const Offset(2, 4),   // Bank
    8: const Offset(4.2, 9),   // Grupo Brisa
    9: const Offset(2, 13),  // Hospital
    10: const Offset(3.5, 15.2),
    11: const Offset(5.5, 16),
    12: const Offset(7.5, 15.8),
    13: const Offset(10, 15.8),
    14: const Offset(8, 14.5),
    15: const Offset(7.5, 8.5),
  };

  // Ajustes finos individuais de posição para cada um dos 16 ArUcos (dx, dy em células)
  final Map<int, Offset> arucoCustomOffsets = {
    0: const Offset(0.0, 0.0), // 42 Porto
    1: const Offset(-0.95, -0.9), // Sea:Me
    2: const Offset(0.0, 0.0),   // Interseção
    3: const Offset(-0.95, 0.0), // Gelato
    4: const Offset(0.6, 0.2),   // Padle
    5: const Offset(-0.2, 0.2),   // Pista
    6: const Offset(-0.8, 0.2),   // Climbing
    7: const Offset(0.2, 0.0),   // Bank
    8: const Offset(0.0, 0.0),   // Grupo Brisa
    9: const Offset(0.8, 0.0),   // Hospital
    10: const Offset(0.0, 0.0),  // Pista
    11: const Offset(0.0, 0.0),  // Pista
    12: const Offset(0.0, 0.0),  // Pista
    13: const Offset(0.0, 0.0),  // Pista
    14: const Offset(-0.5, 0.0),  // Pista
    15: const Offset(0.0, 0.0),  // Pista
  };

  // Nomes dos edifícios mapeados por coordenada
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

  // Mapeamento das imagens PNG
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
  
  // Posição e orientação direcional do veículo
  Offset? carPosition = const Offset(7.5, 8.5); 
  double carAngle = 0.0; 
  Offset? _lastCarPosition;
  int? currentArucoId = 15;
  double currentArucoDistanceCm = 0.0;

  // Gerenciamento de rede
  String serverIp = "10.21.220.182:8000";
  WebSocket? _webSocket;
  bool isConnected = false;
  String robotStatus = "Desconected";
  String missionState = "None";
  String lastArUcoDetected = "None";

  @override
  void initState() {
    super.initState();
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
      robotStatus = "Conectando...";
    });

    try {
      final cleanIp = _getSanitizedIp();
      final wsUrl = "ws://$cleanIp/ws/frontend";
      _webSocket = await WebSocket.connect(wsUrl).timeout(const Duration(seconds: 4));
      
      setState(() {
        isConnected = true;
        robotStatus = "Conectado";
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
        robotStatus = "Desconected";
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
            currentArucoId = (arucoData["id"] as num).toInt();
            currentArucoDistanceCm = (arucoData["distance_cm"] as num?)?.toDouble() ?? 0.0;
            lastArUcoDetected = "ID $currentArucoId (${currentArucoDistanceCm.toStringAsFixed(1)} cm)";
          } else {
            currentArucoId = null;
            currentArucoDistanceCm = 0.0;
            lastArUcoDetected = "None";
          }

          final currentGrid = telemetry["current_grid"];
          if (currentGrid != null) {
            final double newCol = (currentGrid["col"] as num).toDouble();
            final double newRow = (currentGrid["row"] as num).toDouble();
            
            // Ajuste fino de distância do ArUco para o movimento não dar pulos bruscos
            double distanceCellOffset = 0.0;
            if (currentArucoDistanceCm > 0) {
              distanceCellOffset = (currentArucoDistanceCm / cmPerCell).clamp(0.0, 1.5);
            }

            // Desloca o carro gradualmente na direção da trajetória baseada na distância
            double targetCol = newCol;
            double targetRow = newRow;

            if (_lastCarPosition != null) {
              double dx = newCol - _lastCarPosition!.dx;
              double dy = newRow - _lastCarPosition!.dy;
              if (dx != 0 || dy != 0) {
                carAngle = atan2(dy, dx);
                // Subtrai a distância do ArUco na direção do vetor de movimento
                targetCol -= cos(carAngle) * distanceCellOffset;
                targetRow -= sin(carAngle) * distanceCellOffset;
              }
            }

            final Offset newPos = Offset(targetCol, targetRow);
            _lastCarPosition = carPosition;
            carPosition = newPos;
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
            content: Text("Enviado: $payloadJson"),
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
          content: Text("Falha ao enviar ($payloadJson): $e"),
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

    Offset arucoOffset = (currentArucoId != null && arucoCustomOffsets.containsKey(currentArucoId))
        ? arucoCustomOffsets[currentArucoId]!
        : const Offset(0, 0);

    double carLeft = 0;
    double carTop = 0;

    if (carPosition != null) {
      double effectiveCol = carPosition!.dx + carGlobalOffset.dx + arucoOffset.dx;
      double effectiveRow = carPosition!.dy + carGlobalOffset.dy + arucoOffset.dy;

      carLeft = (effectiveCol * cellSize) - (carWidth - cellSize) / 2;
      carTop = (effectiveRow * cellSize) - (carHeight - cellSize) / 2;
    }

    return Scaffold(
      backgroundColor: const Color(0xFF121214),
      appBar: AppBar(
        title: const Text('Robotáxi Prototipador', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.black26,
        centerTitle: true,
        actions: [
          IconButton(
            tooltip: "Modo Calibração ArUco",
            icon: Icon(Icons.bug_report, color: showDebugArUcos ? Colors.blueAccent : Colors.grey),
            onPressed: () => setState(() => showDebugArUcos = !showDebugArUcos),
          ),
          IconButton(
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
                        // Camada 1: Imagem do mapa
                        Image.asset(
                          'assets/mapa.png',
                          width: mapWidth,
                          height: mapHeight,
                          fit: BoxFit.fill,
                        ),

                        // Camada 1.5: Caixas azuis de depuração para TODOS OS 16 ARUCOS
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

                        // Camada 2: Renderização dos edifícios selecionados
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

                        // Camada 3: Carrinho animado com deslize de 800ms suave
                        if (carPosition != null)
                          AnimatedPositioned(
                            duration: const Duration(milliseconds: 800),
                            curve: Curves.easeInOut,
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
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.05),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
      ),
      child: Column(
        children: [
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
              labelText: "Server IP and Port (e.g., 192.168.1.20:8000)",
              labelStyle: TextStyle(color: Colors.white60),
              enabledBorder: UnderlineInputBorder(borderSide: BorderSide(color: Colors.white24)),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text("Cancelar", style: TextStyle(color: Colors.grey)),
            ),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  serverIp = controller.text;
                });
                Navigator.pop(context);
                _connectWebSocket();
              },
              child: const Text("Salvar e Conectar"),
            )
          ],
        );
      },
    );
  }
}
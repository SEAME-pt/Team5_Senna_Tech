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

  // Mapeamento das imagens PNG na pasta assets/
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

  // Ajustes individuais de deslocamento em células (dx, dy) para calibrar posição do PNG caso precise
  final Map<Offset, Offset> buildingCustomOffsets = {
    const Offset(5, 1): const Offset(-0.5, -0.5),//climbing
    const Offset(9, 1): const Offset(0.3, -0.3),//padle
    const Offset(1, 4): const Offset(-0.5, -0.2),//bank
    const Offset(13, 4): const Offset(0.0, 0.0),//gelado
    const Offset(2, 9): const Offset(-0.6, -0.2),//brisa
    const Offset(13, 9): const Offset(0.0, 0.0),//seame
    const Offset(13, 14): const Offset(0.2, -1),//42porto
    const Offset(1, 13): const Offset(0.0, 0.0),//hospital
  };

  // Multiplicador de escala individual do tamanho do PNG
  final Map<Offset, double> buildingSizes = {
    const Offset(5, 1): 2.8,//climbing
    const Offset(9, 1): 4.2,//padle
    const Offset(1, 4): 2.8,//bank
    const Offset(13, 4): 2.8,//gelado
    const Offset(2, 9): 3.3,//brisa
    const Offset(13, 9): 3.0,//seame
    const Offset(13, 14): 3.2,//42porto
    const Offset(1, 13): 2.8,//hospital
  };

  // IDs dos ArUcos físicos esperados pelo servidor Python
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
  Offset? carPosition = const Offset(7.5, 8); 
  double carAngle = 0.0; 
  Offset? _lastCarPosition;

  // Gerenciamento da comunicação de rede
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
    if (clean.endsWith('/ws/robotaxi')) {
      clean = clean.replaceAll('/ws/robotaxi', '');
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
      final wsUrl = "ws://$cleanIp/ws/robotaxi";
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
            lastArUcoDetected = "ID ${arucoData["id"]} (${arucoData["distance_cm"]} cm)";
          } else {
            lastArUcoDetected = "None";
          }

          final currentGrid = telemetry["current_grid"];
          if (currentGrid != null) {
            final double newCol = (currentGrid["col"] as num).toDouble();
            final double newRow = (currentGrid["row"] as num).toDouble();
            final Offset newPos = Offset(newCol, newRow);

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

    print("$payloadJson");

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

    return Scaffold(
      backgroundColor: const Color(0xFF121214),
      appBar: AppBar(
        title: const Text('Robotáxi Prototipador', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.black26,
        centerTitle: true,
        actions: [
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
                        // Camada 1: Imagem de fundo completa do mapa
                        Image.asset(
                          'assets/mapa.png',
                          width: mapWidth,
                          height: mapHeight,
                          fit: BoxFit.fill,
                        ),

                        // Camada 2: Renderização limpa apenas do Prédio SELECIONADO (Com contorno justo e sem miniaturas)
                        ...buildingAssets.entries.map((entry) {
                          final Offset pos = entry.key;
                          final String assetPath = entry.value;

                          final bool isPickup = pickupPoint == pos;
                          final bool isDropoff = dropoffPoint == pos;
                          final bool isSelected = isPickup || isDropoff;

                          // Se não estiver selecionado, não renderiza nada (evita duplicar imagem sobre o mapa)
                          if (!isSelected) return const SizedBox.shrink();

                          final Offset customOffset = buildingCustomOffsets[pos] ?? const Offset(0, 0);
                          final double scaleMultiplier = buildingSizes[pos] ?? 2.2;

                          final double buildingWidth = cellSize * scaleMultiplier;
                          final double buildingHeight = cellSize * scaleMultiplier;

                          final double posX = ((pos.dx + customOffset.dx) * cellSize) - (buildingWidth - cellSize) / 2;
                          final double posY = ((pos.dy + customOffset.dy) * cellSize) - (buildingHeight - cellSize) / 2;

                          final Color accentColor = isPickup ? Colors.greenAccent : Colors.redAccent;
                          
                          // Distância reduzida para 1.2px: cria um contorno (outline) perfeito em volta do PNG sem parecer miniatura duplicada
                          const double strokeOffset = 1.2;

                          return Positioned(
                            left: posX,
                            top: posY,
                            child: IgnorePointer(
                              child: AnimatedScale(
                                duration: const Duration(milliseconds: 300),
                                curve: Curves.easeOutBack,
                                scale: 1.3, // Expande suavemente em 3D sobre o prédio do mapa
                                child: SizedBox(
                                  width: buildingWidth,
                                  height: buildingHeight,
                                  child: Stack(
                                    alignment: Alignment.center,
                                    children: [
                                      // 1. Sombra de profundidade que cobre o prédio do mapa para evitar transparência/imagem dupla
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

                                      // 2. Réplicas justas (1.2px) nas 8 direções para criar o contorno (outline) perfeito
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

                                      // 3. Foto original do prédio perfeitamente nítida por cima
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

                        // Camada 3: Carrinho animado com rotação
                        if (carPosition != null)
                          AnimatedPositioned(
                            duration: const Duration(milliseconds: 350),
                            curve: Curves.easeInOut,
                            left: carPosition!.dx * cellSize,
                            top: carPosition!.dy * cellSize,
                            child: Transform.rotate(
                              angle: carAngle,
                              child: Container(
                                padding: const EdgeInsets.all(2),
                                width: cellSize,
                                height: cellSize,
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
              Text("Back-end status: $robotStatus", style: TextStyle(color: isConnected ? Colors.greenAccent : Colors.redAccent, fontSize: 12, fontWeight: FontWeight.bold)),
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
                  'Drop-off: ${_getBuildingName(dropoffPoint)}',
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
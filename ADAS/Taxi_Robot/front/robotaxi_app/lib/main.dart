import 'package:flutter/material.dart';
import 'dart:math';

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
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], // Linha 0 (Apenas 2 ArUcos do topo: Col 3 e Col 12)
    [1, 0, 0, 0, 1, 5, 1, 1, 1, 5, 1, 1, 1, 0, 0], // Linha 1 (ArUcos do norte agora estão na Linha 1, Col 5 e Col 9)
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], // Linha 2
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], // Linha 3
    [1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 0], // Linha 4 (Prédio Roxo Col 1, Café Azul Col 13)
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], // Linha 5
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], // Linha 6
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], // Linha 7
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0], // Linha 8
    [1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 0], // Linha 9 (Prédio Brisa Col 2)
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0], // Linha 10 (Sea Me Col 13)
    [1, 1, 1, 1, 0, 0, 5, 1, 0, 0, 5, 1, 1, 1, 0], // Linha 11 (Residencial Verde Col 6, Bombeiros Col 10)
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1], // Linha 12
    [1, 5, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0], // Linha 13
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 5, 1, 1, 5, 0], // Linha 14 (42 Porto Col 13)
    [1, 1, 1, 0, 0, 5, 1, 0, 2, 0, 1, 1, 1, 1, 0], // Linha 15 (RS Col 1, Mercado24h Col 5, CasaModerna Col 10)
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0], // Linha 16
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1], // Linha 17
    [1, 1, 1, 1, 1, 1, 2, 0, 0, 2, 0, 2, 0, 0, 1], // Linha 18
  ];

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

  Offset? pickupPoint;
  Offset? dropoffPoint;
  Offset? carPosition = const Offset(5, 0); // Posição inicial no norte da pista

  void handleTap(TapUpDetails details, double cellSize) {
    double tappedCol = details.localPosition.dx / cellSize;
    double tappedRow = details.localPosition.dy / cellSize;

    double minDistance = double.infinity;
    Offset? closestBuilding;

    // Busca o ArUco (5) mais próximo na nova matriz
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

    // Se o clique foi próximo (raio de 2.2 blocos), atrai a seleção para ele!
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
    if (point == null) return "Pendente";
    return buildingNames[point] ?? "Edifício [${point.dx.toInt()},${point.dy.toInt()}]";
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    if (screenWidth > 500) screenWidth = 400; // Preserva visual mobile no computador
    
    double cellSize = (screenWidth - 32) / 15;
    double mapHeight = cellSize * 19;
    double mapWidth = cellSize * 15;

    // Tamanho customizado dos pins e ícones
    double pinSize = cellSize * 1.5;

    return Scaffold(
      backgroundColor: const Color(0xFF121214),
      appBar: AppBar(
        title: const Text('Robotáxi Prototipador', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.black26,
        centerTitle: true,
      ),
      body: Center(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
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
                        // Camada de Fundo do Canva
                        Image.asset(
                          'assets/mapa.png',
                          width: mapWidth,
                          height: mapHeight,
                          fit: BoxFit.fill,
                        ),

                        // Camada de Debug (Garante o brilho ao redor de quem foi selecionado)
                        Positioned.fill(
                          child: CustomPaint(
                            painter: DebugGridPainter(
                              matrix: mapGrid, 
                              cellSize: cellSize,
                              pickup: pickupPoint,
                              dropoff: dropoffPoint,
                            ),
                          ),
                        ),

                        // Marcador de Coleta (Pickup) ampliado e centralizado
                        if (pickupPoint != null)
                          Positioned(
                            left: (pickupPoint!.dx * cellSize) + (cellSize - pinSize) / 2,
                            top: (pickupPoint!.dy * cellSize) - (pinSize) + (cellSize / 2),
                            child: SizedBox(
                              width: pinSize,
                              height: pinSize,
                              child: const Icon(
                                Icons.location_on, 
                                color: Colors.greenAccent, 
                                size: 38,
                                shadows: [Shadow(color: Colors.black45, blurRadius: 4, offset: Offset(0, 3))],
                              ),
                            ),
                          ),
                          
                        // Marcador de Destino (Dropoff) ampliado e centralizado
                        if (dropoffPoint != null)
                          Positioned(
                            left: (dropoffPoint!.dx * cellSize) + (cellSize - pinSize) / 2,
                            top: (dropoffPoint!.dy * cellSize) - (pinSize) + (cellSize / 2),
                            child: SizedBox(
                              width: pinSize,
                              height: pinSize,
                              child: const Icon(
                                Icons.flag, 
                                color: Colors.redAccent, 
                                size: 38,
                                shadows: [Shadow(color: Colors.black45, blurRadius: 4, offset: Offset(0, 3))],
                              ),
                            ),
                          ),

                        // Carrinho customizado
                        if (carPosition != null)
                          Positioned(
                            left: carPosition!.dx * cellSize,
                            top: carPosition!.dy * cellSize,
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
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 12),
                TextButton.icon(
                  onPressed: () {
                    setState(() {
                      pickupPoint = null;
                      dropoffPoint = null;
                    });
                  },
                  icon: const Icon(Icons.refresh, color: Colors.grey),
                  label: const Text('Resetar Seleções', style: TextStyle(color: Colors.grey)),
                )
              ],
            ),
          ),
        ),
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
                  'Coleta: ${_getBuildingName(pickupPoint)}',
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
                  'Destino: ${_getBuildingName(dropoffPoint)}',
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
}

class DebugGridPainter extends CustomPainter {
  final List<List<int>> matrix;
  final double cellSize;
  final Offset? pickup;
  final Offset? dropoff;

  DebugGridPainter({
    required this.matrix, 
    required this.cellSize,
    this.pickup,
    this.dropoff,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..style = PaintingStyle.fill;
    final borderPaint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    for (int r = 0; r < 19; r++) {
      for (int c = 0; c < 15; c++) {
        Rect rect = Rect.fromLTWH(c * cellSize, r * cellSize, cellSize, cellSize);

        // Se este prédio específico for o ponto de COLETA, desenha um neon verde brilhante ao redor dele
        if (pickup != null && pickup!.dx.toInt() == c && pickup!.dy.toInt() == r) {
          paint.color = Colors.greenAccent.withValues(alpha: 0.15);
          canvas.drawRect(rect, paint);
          
          borderPaint.color = Colors.greenAccent;
          canvas.drawRect(rect, borderPaint);
        } 
        // Se for o ponto de DESTINO, desenha um neon vermelho brilhante
        else if (dropoff != null && dropoff!.dx.toInt() == c && dropoff!.dy.toInt() == r) {
          paint.color = Colors.redAccent.withValues(alpha: 0.15);
          canvas.drawRect(rect, paint);
          
          borderPaint.color = Colors.redAccent;
          canvas.drawRect(rect, borderPaint);
        }
        // Prédios comuns não-selecionados (mostra apenas uma borda laranja discreta como guia)
        else if (matrix[r][c] == 5) {
          paint.color = Colors.orange.withValues(alpha: 0.05);
          canvas.drawRect(rect, paint);
          
          final guidePaint = Paint()
            ..style = PaintingStyle.stroke
            ..color = Colors.orange.withValues(alpha: 0.3)
            ..strokeWidth = 1.0;
          canvas.drawRect(rect, guidePaint);
        }
      }
    }
  }

  @override
  bool shouldRepaint(covariant DebugGridPainter oldDelegate) {
    return oldDelegate.pickup != pickup || oldDelegate.dropoff != dropoff;
  }
}
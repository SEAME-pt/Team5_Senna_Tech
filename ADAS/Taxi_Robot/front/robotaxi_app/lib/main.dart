import 'package:flutter/material.dart';

// 1. Criamos a classe MyApp que o arquivo de teste (test/widget_test.dart) estava procurando
void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false, // Remove a faixa de debug do canto da tela
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
  // Sua matriz exata para validação dos cliques
  final List<List<int>> mapGrid = [
    [1, 1, 1, 5, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [5, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 5, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 5],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 5, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 0, 2, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 5],
    [1, 1, 1, 1, 1, 1, 2, 0, 0, 2, 0, 2, 0, 0, 1],
  ];

  Offset? pickupPoint;
  Offset? dropoffPoint;
  Offset? carPosition = const Offset(4, 0); // Carro começa na pista (linha 0, col 4)

  void handleTap(TapUpDetails details, double cellSize) {
    int col = (details.localPosition.dx / cellSize).floor();
    int row = (details.localPosition.dy / cellSize).floor();

    if (row >= 0 && row < 19 && col >= 0 && col < 15) {
      if (mapGrid[row][col] == 5) { 
        setState(() {
          if (pickupPoint == null) {
            pickupPoint = Offset(col.toDouble(), row.toDouble());
          } else if (dropoffPoint == null) {
            dropoffPoint = Offset(col.toDouble(), row.toDouble());
          } else {
            pickupPoint = Offset(col.toDouble(), row.toDouble());
            dropoffPoint = null;
          }
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    if (screenWidth > 500) screenWidth = 400; // Mantém proporção compacta no PC
    
    double cellSize = (screenWidth - 32) / 15;
    double mapHeight = cellSize * 19;
    double mapWidth = cellSize * 15;

    return Scaffold(
      backgroundColor: const Color(0xFF121214),
      appBar: AppBar(
        title: const Text('Robotáxi Prototipador', style: TextStyle(fontSize: 18)),
        backgroundColor: Colors.black26, // Correção do black24 para black26
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
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.white12),
                    ),
                    child: Stack(
                      children: [
                        Image.network(
                          'https://placehold.co/1500x1900/1e1e24/1e1e24',
                          width: mapWidth,
                          height: mapHeight,
                          fit: BoxFit.fill,
                        ),

                        Positioned.fill(
                          child: CustomPaint(
                            painter: DebugGridPainter(matrix: mapGrid, cellSize: cellSize),
                          ),
                        ),

                        if (pickupPoint != null)
                          Positioned(
                            left: pickupPoint!.dx * cellSize,
                            top: pickupPoint!.dy * cellSize,
                            child: SizedBox(
                              width: cellSize,
                              height: cellSize,
                              child: const Icon(Icons.location_on, color: Colors.greenAccent, size: 22),
                            ),
                          ),
                          
                        if (dropoffPoint != null)
                          Positioned(
                            left: dropoffPoint!.dx * cellSize,
                            top: dropoffPoint!.dy * cellSize,
                            child: SizedBox(
                              width: cellSize,
                              height: cellSize,
                              child: const Icon(Icons.flag, color: Colors.redAccent, size: 22),
                            ),
                          ),

                        if (carPosition != null)
                          Positioned(
                            left: carPosition!.dx * cellSize,
                            top: carPosition!.dy * cellSize,
                            child: SizedBox(
                              width: cellSize,
                              height: cellSize,
                              child: const Icon(Icons.directions_car, color: Colors.cyanAccent, size: 20),
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
                  label: const Text('Resetar Pontos', style: TextStyle(color: Colors.grey)),
                )
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildStatusPanel() {
    // Correção: Atualizado de .withOpacity() para o novo padrão .withValues()
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 16),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.05), 
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          Text(
            'Coleta (5): ${pickupPoint != null ? "[${pickupPoint!.dx.toInt()},${pickupPoint!.dy.toInt()}]" : "Pendente"}',
            style: TextStyle(color: pickupPoint != null ? Colors.greenAccent : Colors.white60, fontSize: 13),
          ),
          Text(
            'Destino (5): ${dropoffPoint != null ? "[${dropoffPoint!.dx.toInt()},${dropoffPoint!.dy.toInt()}]" : "Pendente"}',
            style: TextStyle(color: dropoffPoint != null ? Colors.redAccent : Colors.white60, fontSize: 13),
          ),
        ],
      ),
    );
  }
}

class DebugGridPainter extends CustomPainter {
  final List<List<int>> matrix;
  final double cellSize;

  DebugGridPainter({required this.matrix, required this.cellSize});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..style = PaintingStyle.fill;
    
    // Correção: Substituído .withOpacity() por .withValues() em todos os pincéis
    final strokePaint = Paint()
      ..style = PaintingStyle.stroke
      ..color = Colors.white.withValues(alpha: 0.05)
      ..strokeWidth = 0.5;

    for (int r = 0; r < 19; r++) {
      for (int c = 0; c < 15; c++) {
        Rect rect = Rect.fromLTWH(c * cellSize, r * cellSize, cellSize, cellSize);

        if (matrix[r][c] == 0 || matrix[r][c] == 2) {
          paint.color = Colors.white.withValues(alpha: 0.08);
          canvas.drawRect(rect, paint);
        } else if (matrix[r][c] == 5) {
          paint.color = Colors.orange.withValues(alpha: 0.25);
          canvas.drawRect(rect, paint);
          
          paint.color = Colors.orange.withValues(alpha: 0.6);
          paint.style = PaintingStyle.stroke;
          canvas.drawRect(rect, paint);
          paint.style = PaintingStyle.fill;
        }

        canvas.drawRect(rect, strokePaint);
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
# Object Post-Processing

## Index
- [Overview](#overview)
- [Classes](#classes)
- [Data Contract](#data-contract)
- [Notes](#notes)

## Overview
Trata os outputs crus do modelo de object detection, gera bounding boxes e classifica cada detecção para uso na decisão.

## Classes

### `ObjectDetector`
Responsável por decodificar os tensores do modelo de objetos, aplicar NMS e desenhar as detecções.

#### `__init__()`
Inicializa nomes de classes e limiares de confiança e NMS.

**Efeitos**
- Define a lista de classes suportadas.
- Define os thresholds usados no decode e na supressão de caixas.

#### `sigmoid(x)`
Aplica a função sigmóide aos logits de classe.

#### `make_grid(h, w)`
Cria a grelha espacial usada para transformar offsets em coordenadas absolutas.

#### `decode_output(bbox, cls, stride)`
Converte um cabeçalho da rede em caixas, scores e classes já filtrados por confiança.

**Comportamento**
- Aplica sigmóide às classes.
- Constrói a grelha espacial.
- Converte offsets em bounding boxes no espaço da imagem.
- Filtra por confiança.

**Saída**
- `boxes`, `scores`, `classes` filtrados.

#### `nms(boxes, scores)`
Aplica Non-Maximum Suppression para remover caixas sobrepostas.

**Comportamento**
- Lê os tensores por escala do modelo.
- Converte offsets e classes em bounding boxes no espaço da imagem.
- Filtra por confiança.
- Aplica NMS para eliminar deteções sobrepostas.
- Reescala as caixas para o tamanho original do frame.

**Saída**
- Índices das caixas mantidas.

#### `process(outputs, frame_shape)`
Decodifica os tensores crus da inferência e devolve uma lista de detecções estruturadas.

**Entradas**
- `outputs`: tensores crus da inferência do modelo de objetos.
- `frame_shape`: shape do frame original usado para reescalamento.

**Saída**
- Lista de dicionários com `bbox`, `score`, `class_id` e `class_name`.

#### `draw(frame, detections)`
Desenha bounding boxes e labels sobre o frame.

**Comportamento**
- Percorre cada detecção já estruturada.
- Escolhe cor e espessura conforme `in_corridor`.
- Desenha retângulos, labels e pontos de referência visual.

**Entrada**
- `frame`: imagem BGR onde os overlays serão desenhados.
- `detections`: lista de detecções produzidas por `process`.

**Saída**
- Frame anotado com as caixas e labels.

### `CorridorChecker`
Responsável por avaliar se uma detecção está dentro do corredor da faixa usando a transformação BEV.

#### `__init__(bev_transform)`
Guarda a transformada BEV usada para mapear pontos do frame para coordenadas da via.

**Efeitos**
- Mantém uma referência ao objeto de transformação que expõe a matriz `M`.

#### `map_point_to_bev(x, y)`
Converte um ponto do frame original para coordenadas BEV.

**Saída**
- Ponto transformado em BEV.

#### `check_and_debug(bbox, fit_result, frame_shape)`
Determina se a detecção está dentro do corredor da faixa e gera dados de debug.

**Comportamento**
- Mapeia o centro inferior da bbox para coordenadas BEV.
- Calcula a área relativa do objeto na imagem.
- Compara a posição da detecção com as linhas estimadas do corredor.
- Retorna um dicionário com flags de presença no corredor e valores de debug.

**Entradas**
- `bbox`: bounding box da detecção.
- `fit_result`: resultado do ajuste das faixas.
- `frame_shape`: shape do frame original.

**Saída**
- `dict` com `in_corridor`, `rel_area` e métricas auxiliares de debug.

## Data Contract
| Field | Type | Meaning |
|---|---|---|
| `outputs_obj` | `dict` | Tensores crus do modelo de object detection |
| `detections` | `list[dict]` | Lista de bounding boxes, scores e classes |
| `EnvironmentState` | `dataclass` | Estado agregado para decisão |

## Notes
- Esta camada prepara as detecções para o `decision` e para as verificações de corredor.

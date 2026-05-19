# Post-Processing

## Index
- [Overview](#overview)
- [Submodules](#submodules)
- [Data Contract](#data-contract)
- [Execution Flow](#execution-flow)
- [Notes](#notes)

## Overview
Esta camada traduz os outputs crus da inferência para estruturas de domínio usadas pelo restante da pipeline.

Ela está dividida em dois subdomínios:
- `lane` para segmentação de faixa e limpeza de máscara
- `object` para detecção de objetos e verificação de corredor

## Submodules
- [Lane Post-Processing](lane/README.md)
- [Object Post-Processing](object/README.md)

## Input
| Field | Type | Meaning |
|---|---|---|
| `outputs_lane` | `dict` | Tensores crus do modelo de lane segmentation |
| `outputs_obj` | `dict` | Tensores crus do modelo de object detection |

## Output
| Field | Type | Meaning |
|---|---|---|
| `binary_mask` | `numpy.ndarray uint8` | Máscara binária tratada para LFA |
| `detections` | `list[dict]` | Lista de detecções estruturadas para decisão |

## Data Contract
| Field | Type | Meaning |
|---|---|---|
| `outputs_lane` | `dict` | Entrada da subcamada `lane` |
| `outputs_obj` | `dict` | Entrada da subcamada `object` |
| `binary_mask` | `numpy.ndarray uint8` | Saída da subcamada `lane` |
| `detections` | `list[dict]` | Saída da subcamada `object` |

## Execution Flow
- `outputs_lane` -> `lane/YoloSegDecoder.decode_to_mask(...)`
- `binary_mask` -> `lane/MaskFilters.process(...)`
- `outputs_obj` -> `object/ObjectDetector.process(...)`
- `detections` -> `object/CorridorChecker.check_and_debug(...)`

## Notes
- Esta camada fica entre `inference` e os módulos de geometria/decisão.
- Os detalhes de cada modelo ficam encapsulados nos submódulos correspondentes.

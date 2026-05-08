# 04 — BEV Transform

## Responsabilidade
Transforma a máscara binária de perspetiva frontal para vista top-down (Bird's Eye View), permitindo medir distâncias reais na estrada.

## Módulo
- **`BEVTransform`** — transformação de perspetiva via `cv2.getPerspectiveTransform`

## Input
| Campo | Tipo | Shape |
|---|---|---|
| `binary_mask` | `numpy.ndarray uint8` | `(H, W)` |

## Output
| Campo | Tipo | Shape |
|---|---|---|
| `bev_mask` | `numpy.ndarray uint8` | `(H, W)` |

## Observações
- Requer calibração prévia (`src_points` e `dst_points`)
- A preencher durante os testes

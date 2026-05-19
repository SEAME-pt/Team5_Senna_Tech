# Pipeline Interfaces — Visão Geral

## Fluxo de Dados

| Etapa | Módulo | Input | Output |
|---|---|---|---|
| 01 | Camera | — | `rgb (H, W, 3) uint8` |
| 02 | Inference | `rgb` | `outputs_lane (dict)`, `outputs_obj (dict)` |
| 03 | Post-Processing | `outputs_lane` | `binary_mask (H, W) uint8` |
| 04 | BEV Transform | `binary_mask` | `bev_mask (H, W) uint8` |
| 05 | Sliding Windows | `bev_mask` | `fit_result (LaneFitResult)` |
| 06 | CTE | `fit_result.cte_norm` | `cte (float [-1, 1])` |
| 07 | PID | `cte`, `dt` | `pid_return (float [-1, 1])` |
| 08 | CAN Bus | `pid_return`, `current_state` | comando CAN `0x110`, `0x001` |

## Documentação por módulo
- [Camera](../camera/README.md)
- [Inference](../inference/README.md)
- [Post-Processing](../post_processing/README.md)
- [LFA Geometry](../LFA/geometry/README.md)
- [LFA](../LFA/README.md)
- [Decision](../decision/README.md)
- [Utils](../utils/README.md)

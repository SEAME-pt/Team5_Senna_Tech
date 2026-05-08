# Pipeline Interfaces — Visão Geral

## Fluxo de Dados

| Etapa | Módulo | Input | Output |
|---|---|---|---|
| 01 | Camera | — | `bgr (H, W, 3) uint8` |
| 02 | Inference | `bgr` | `outputs_lane (dict)`, `outputs_obj (dict)` |
| 03 | Post-Processing | `outputs_lane` | `binary_mask (H, W) uint8` |
| 04 | BEV Transform | `binary_mask` | `bev_mask (H, W) uint8` |
| 05 | Sliding Windows | `bev_mask` | `fit_result (LaneFitResult)` |
| 06 | CTE | `fit_result.cte_norm` | `cte (float [-1, 1])` |
| 07 | PID | `cte`, `dt` | `pid_return (float [-1, 1])` |
| 08 | CAN Bus | `pid_return`, `current_state` | comando CAN `0x110`, `0x001` |

## Documentação por módulo
- [01 — Camera](01_camera.md)
- [02 — Inference](02_inference.md)
- [03 — Post-Processing](03_postprocess.md)
- [04 — BEV Transform](04_bev.md)
- [05 — Sliding Windows](05_sliding_windows.md)
- [06 — CTE](06_cte.md)
- [07 — PID](07_pid.md)
- [08 — CAN Bus](08_can.md)

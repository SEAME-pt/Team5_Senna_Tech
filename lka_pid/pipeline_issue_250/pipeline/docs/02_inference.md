# 02 — Inference

## Responsabilidade
Executa os dois modelos YOLO26 no acelerador Hailo-8 e devolve os tensores crus.

## Hardware
- **Acelerador:** Hailo-8 NPU
- **Modelos:** `yolo26n_seg_640.hef` (LKA), `yolo26n_v4.hef` (Object Detection)

## Input
| Campo | Tipo | Shape |
|---|---|---|
| `rgb` | `numpy.ndarray uint8` | `(H, W, 3)` |

## Output
| Campo | Tipo | Descrição |
|---|---|---|
| `outputs_lane` | `dict` | 4 tensores crus do modelo LKA |
| `outputs_obj` | `dict` | 6 tensores crus do modelo Object Detection |

## Observações
- A preencher durante os testes

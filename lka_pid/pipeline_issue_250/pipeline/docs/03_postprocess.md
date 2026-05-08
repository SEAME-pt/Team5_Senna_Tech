# 03 — Post-Processing

## Responsabilidade
Converte os tensores crus do modelo LKA numa máscara binária limpa das faixas de rodagem.

## Módulos
- **`YoloSegDecoder`** — decode dos tensores → máscara binária
- **`MaskFilters`** — limpeza morfológica (MORPH_CLOSE + MORPH_OPEN)

## Input
| Campo | Tipo | Descrição |
|---|---|---|
| `outputs_lane` | `dict` | 4 tensores crus do modelo LKA |

## Output
| Campo | Tipo | Shape |
|---|---|---|
| `binary_mask` | `numpy.ndarray uint8` | `(H, W)` |

## Observações
- A preencher durante os testes

# 05 — Sliding Windows

## Responsabilidade
Localiza as faixas esquerda e direita na imagem BEV e ajusta polinómios de 2º grau a cada uma.

## Módulo
- **`SlidingWindowsLaneFitter`** — histograma + 9 janelas deslizantes + polyfit

## Input
| Campo | Tipo | Shape |
|---|---|---|
| `bev_mask` | `numpy.ndarray uint8` | `(H, W)` |

## Output
| Campo | Tipo | Descrição |
|---|---|---|
| `fit_result` | `LaneFitResult` | Polinómios left/right + CTE |
| `fit_result.left_fit` | `numpy.ndarray` ou `None` | Coeficientes polinómio esquerdo |
| `fit_result.right_fit` | `numpy.ndarray` ou `None` | Coeficientes polinómio direito |
| `fit_result.cte_norm` | `float` ou `None` | CTE normalizado `[-1, 1]` |

## Observações
- A preencher durante os testes

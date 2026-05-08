# 06 — CTE (Cross-Track Error)

## Responsabilidade
Extrai o erro lateral normalizado do resultado do Sliding Windows. Representa o desvio do veículo em relação ao centro da faixa.

## Input
| Campo | Tipo | Descrição |
|---|---|---|
| `fit_result.cte_norm` | `float` ou `None` | CTE calculado pelo Sliding Windows |

## Output
| Campo | Tipo | Descrição |
|---|---|---|
| `cte` | `float` | Erro lateral normalizado `[-1, 1]` |

## Comportamento
- `0` — veículo centrado
- Negativo — desvio para a esquerda
- Positivo — desvio para a direita
- Se `cte_norm` for `None` (faixas não detetadas) → fallback `0.0`

## Observações
- A preencher durante os testes

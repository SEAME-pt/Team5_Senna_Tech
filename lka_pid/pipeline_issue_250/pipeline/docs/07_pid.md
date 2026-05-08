# 07 — PID Controller

## Responsabilidade
Calcula o ângulo de steering com base no CTE usando um controlador PID.

## Módulo
- **`PID`** — controlador Proporcional-Integral-Derivativo

## Input
| Campo | Tipo | Descrição |
|---|---|---|
| `cte` | `float` | Erro lateral normalizado `[-1, 1]` |
| `dt` | `float` | Tempo desde o último frame (segundos) |

## Output
| Campo | Tipo | Descrição |
|---|---|---|
| `pid_return` | `float` | Ângulo de steering normalizado `[-1, 1]` |

## Ganhos
| Parâmetro | Valor |
|---|---|
| `kp` | `1.5` |
| `ki` | `0.25` |
| `kd` | `0.15` |

## Observações
- A preencher durante os testes

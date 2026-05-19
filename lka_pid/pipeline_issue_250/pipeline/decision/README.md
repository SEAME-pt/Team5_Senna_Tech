# Decision

## Responsabilidade
Calcula a direção e coordena o comportamento de alto nível da pipeline a partir do erro lateral.

## Módulos
- `PID` - controlador proporcional-integral-derivativo
- `decision_fsm` - máquina de estados para decisões de condução

## Documentação Interna

### 07 - PID Controller
Calcula o ângulo de steering com base no CTE usando um controlador PID.

#### Input
| Campo | Tipo | Descrição |
|---|---|---|
| `cte` | `float` | Erro lateral normalizado `[-1, 1]` |
| `dt` | `float` | Tempo desde o último frame (segundos) |

#### Output
| Campo | Tipo | Descrição |
|---|---|---|
| `pid_return` | `float` | Ângulo de steering normalizado `[-1, 1]` |

#### Ganhos
| Parâmetro | Valor |
|---|---|
| `kp` | `1.5` |
| `ki` | `0.25` |
| `kd` | `0.15` |

#### Observações
- A preencher durante os testes

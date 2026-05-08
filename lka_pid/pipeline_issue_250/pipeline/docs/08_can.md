# 08 — CAN Bus

## Responsabilidade
Envia o comando de steering para o veículo via barramento CAN.

## Módulo
- **`CanSender`** — interface CAN via `socketcan`

## Input
| Campo | Tipo | Descrição |
|---|---|---|
| `pid_return` | `float` | Ângulo de steering normalizado `[-1, 1]` |
| `current_state` | `FSMState` | Estado atual da máquina de estados |

## Output
| Endereço | Descrição |
|---|---|
| `0x110` | Comando de steering (`pid_return * -1`) |
| `0x001` | Estado da FSM |

## Comportamento
- Safety check: só envia se `abs(last_valid_pid - pid_return) <= 0.4`
- Não envia se flag `--virtual` estiver ativa

## Observações
- A preencher durante os testes

# Utils

## Responsabilidade
Reúne utilitários de infraestrutura e integração externa usados pela pipeline.

## Componentes
- `CanSender` - interface CAN via `socketcan`
- `hw_monitor` - monitoramento de hardware

## Documentação Interna

### 08 - CAN Bus
Envia o comando de steering para o veículo via barramento CAN.

#### Input
| Campo | Tipo | Descrição |
|---|---|---|
| `pid_return` | `float` | Ângulo de steering normalizado `[-1, 1]` |
| `current_state` | `FSMState` | Estado atual da máquina de estados |

#### Output
| Endereço | Descrição |
|---|---|
| `0x110` | Comando de steering (`pid_return * -1`) |
| `0x001` | Estado da FSM |

#### Comportamento
- Safety check: só envia se `abs(last_valid_pid - pid_return) <= 0.4`
- Não envia se flag `--virtual` estiver ativa

#### Observações
- A preencher durante os testes

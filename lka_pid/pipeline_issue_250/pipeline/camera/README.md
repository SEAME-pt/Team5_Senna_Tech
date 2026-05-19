# Camera Module

## Index
- [Overview](#overview)
- [Hardware](#hardware)
- [API / Methods](#api--methods)
- [Data Contract](#data-contract)
- [Notes](#notes)

## Overview
Captura frames de vídeo e fornece-os ao pipeline em formato RGB.

## Hardware
- **Modelo:** Raspberry Pi Camera Module 3 (Wide NoIR)
- **Sensor:** Sony IMX708
- **Referência:** https://www.raspberrypi.com/products/camera-module-3/

## API / Methods

### `Camera.__init__(width, height, fps, debug=False)`
Guarda a configuração da câmara e calcula o tamanho esperado de cada frame em bytes.

#### Parâmetros
- `width` e `height` definem a resolução de captura.
- `fps` define a taxa nominal de frames por segundo.
- `debug` ativa logs adicionais por frame.

#### Efeitos
- Inicializa `self.process` como `None`.
- Prepara o tamanho de frame YUV420 usado na leitura do pipe.

### `Camera.__enter__()`
Inicia o processo `rpicam-vid` e prepara a captura contínua.

#### Comportamento
- Verifica se já existe outro processo `rpicam-vid` ativo.
- Se existir, não inicia um segundo processo e apenas devolve a instância.
- Se não existir, executa `rpicam-vid` com saída em pipe (`stdout`).

#### Efeitos
- Cria `self.process` com `subprocess.Popen`.
- Passa a disponibilizar frames para `read_frame()`.

### `Camera.read_frame()`
Lê um frame cru do pipe, converte de YUV420 para RGB e devolve o frame pronto para a pipeline.

#### Comportamento
- Falha de forma segura se a câmera não estiver ativa.
- Lê exatamente o número de bytes esperado por frame.
- Retorna `None` se o pipe não produzir um frame completo.
- Converte o buffer para `numpy.ndarray` e depois para RGB.

#### Saída
- `numpy.ndarray` em RGB com shape `(height, width, 3)`, ou `None` em caso de falha/leitura incompleta.

### `Camera.__exit__(exc_type, exc_val, exc_tb)`
Encerra o processo da câmera ao sair do contexto.

#### Comportamento
- Termina o processo `rpicam-vid`, se ele existir.
- Espera o processo terminar antes de sair.

#### Efeitos
- Libera os recursos do processo capturado pelo contexto.

## Data Contract
| Field | Type | Shape | Meaning |
|---|---|---|---|
| `rgb` | `numpy.ndarray uint8` | `(360, 640, 3)` | Frame entregue ao restante da pipeline |

> O formato nativo da câmara é `YUV420`. O módulo converte internamente para RGB antes de entregar ao pipeline.

## Notes
No fluxo de dados da pipeline, a câmera é a primeira etapa funcional, porque é ela que origina os frames consumidos pelas etapas seguintes.

No entanto, isso não significa que ela precise ser sempre o primeiro recurso a ser inicializado na execução da aplicação. Em cenários onde a inferência depende de hardware dedicado, como a Hailo, pode fazer sentido inicializar primeiro a infraestrutura de inferência e abrir a câmera apenas depois que o sistema estiver pronto para consumir os frames.

Essa distinção é importante:

- no fluxo de dados, a câmera vem primeiro;
- na ordem de inicialização dos recursos, ela pode vir depois da preparação da inferência.

Essa escolha evita abrir a captura contínua sem que o restante da pipeline esteja preparado para processar os dados gerados.

## Configuration
| Parâmetro | Valor | Descrição |
|---|---|---|
| `width` | `640` | Largura do frame |
| `height` | `360` | Altura do frame |
| `fps` | `60` | Frames por segundo |
| `frame_size` | `width * height * 3 // 2` | Tamanho YUV420 em bytes |

## YUV420 Format
O sensor captura em YUV420 — formato raw que separa brilho (Y) da cor (U, V):
- Plano Y: `640 × 360 = 230400 bytes` (1 valor por pixel)
- Plano U: `57600 bytes` (1 valor por cada 4 pixels)
- Plano V: `57600 bytes` (1 valor por cada 4 pixels)
- Total: `345600 bytes` = `640 × 360 × 1.5`

O `reshape((540, 640))` organiza os bytes em matriz onde Y ocupa as primeiras 360 linhas e U+V as restantes 180.
O `cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB_I420)` combina os 3 planos e devolve RGB `(360, 640, 3)`.

Usamos RGB porque é o formato esperado pelos modelos YOLO no Hailo.

> Para aprofundar: [YUV420 format](https://en.wikipedia.org/wiki/YUV#Y%E2%80%B2UV420p_and_Y%E2%80%B2V12_or_YV12_to_RGB888_conversion)

## Notes
- O primeiro frame demora ~400ms (inicialização da câmara), os seguintes ~17ms (~60 FPS)
- FPS dinâmico seria implementável via `@property` setter com reinício do processo
- Se o pipeline crashar abruptamente, o processo `rpicam-vid` pode ficar preso — verificar com `pgrep -f rpicam-vid` e terminar com `kill <PID>`
- O módulo detecta automaticamente processos presos e avisa no log — não mata sem confirmação do utilizador

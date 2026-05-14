# 01 — Camera Module

## Responsabilidade
Captura frames de vídeo e fornece-os ao pipeline em formato RGB.

## Hardware
- **Modelo:** Raspberry Pi Camera Module 3 (Wide NoIR)
- **Sensor:** Sony IMX708
- **Referência:** https://www.raspberrypi.com/products/camera-module-3/

## Input
Nenhum — é a origem do fluxo.

## Output
| Campo | Tipo | Shape |
|---|---|---|
| `rgb` | `numpy.ndarray uint8` | `(360, 640, 3)` |

> **Formato nativo da câmara:** YUV420. O módulo converte internamente para RGB antes de entregar ao pipeline.

## Implementação
- **Classe:** `Camera` em `camera/raspCam.py`
- **Padrão:** Context Manager (`__enter__` / `__exit__`)
- Captura via `rpicam-vid` em formato YUV420 (pipe para stdout)
- Conversão interna: `YUV420 → RGB` via `cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB_I420)`
- `_check_existing()` — método privado que verifica se já existe um processo `rpicam-vid` a correr antes de iniciar, avisa com o PID e não mata automaticamente
- `debug=False` — parâmetro opcional que activa logs detalhados por frame (`[CAMERA] rgb shape: ...`)

## Papel no fluxo e na inicialização
No fluxo de dados da pipeline, a câmera é a primeira etapa funcional, porque é ela que origina os frames consumidos pelas etapas seguintes.

No entanto, isso não significa que ela precise ser sempre o primeiro recurso a ser inicializado na execução da aplicação. Em cenários onde a inferência depende de hardware dedicado, como a Hailo, pode fazer sentido inicializar primeiro a infraestrutura de inferência e abrir a câmera apenas depois que o sistema estiver pronto para consumir os frames.

Essa distinção é importante:

- no fluxo de dados, a câmera vem primeiro;
- na ordem de inicialização dos recursos, ela pode vir depois da preparação da inferência.

Essa escolha evita abrir a captura contínua sem que o restante da pipeline esteja preparado para processar os dados gerados.

## Configuração
| Parâmetro | Valor | Descrição |
|---|---|---|
| `width` | `640` | Largura do frame |
| `height` | `360` | Altura do frame |
| `fps` | `60` | Frames por segundo |
| `frame_size` | `width * height * 3 // 2` | Tamanho YUV420 em bytes |

## Formato YUV420
O sensor captura em YUV420 — formato raw que separa brilho (Y) da cor (U, V):
- Plano Y: `640 × 360 = 230400 bytes` (1 valor por pixel)
- Plano U: `57600 bytes` (1 valor por cada 4 pixels)
- Plano V: `57600 bytes` (1 valor por cada 4 pixels)
- Total: `345600 bytes` = `640 × 360 × 1.5`

O `reshape((540, 640))` organiza os bytes em matriz onde Y ocupa as primeiras 360 linhas e U+V as restantes 180.
O `cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB_I420)` combina os 3 planos e devolve RGB `(360, 640, 3)`.

Usamos RGB porque é o formato esperado pelos modelos YOLO no Hailo.

> Para aprofundar: [YUV420 format](https://en.wikipedia.org/wiki/YUV#Y%E2%80%B2UV420p_and_Y%E2%80%B2V12_or_YV12_to_RGB888_conversion)

## Observações
- O primeiro frame demora ~400ms (inicialização da câmara), os seguintes ~17ms (~60 FPS)
- FPS dinâmico seria implementável via `@property` setter com reinício do processo
- Se o pipeline crashar abruptamente, o processo `rpicam-vid` pode ficar preso — verificar com `pgrep -f rpicam-vid` e terminar com `kill <PID>`
- O módulo detecta automaticamente processos presos e avisa no log — não mata sem confirmação do utilizador

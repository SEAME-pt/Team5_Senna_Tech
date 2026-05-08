# ADAS Pipeline — Visão Geral

## Etapa 1 — Entrada de Dados (Câmara / Frames)

A primeira etapa da pipeline é a captura dos frames que serão utilizados para inferência pelo modelo de deteção. A origem dos frames e o fluxo de entrada variam consoante o ambiente de execução:

- **Simulador CARLA** — câmara virtual RGB (640×360, FOV 102°), frames capturados diretamente pela API Python do CARLA. O modelo utilizado é o `.pt` (PyTorch), correndo em PC.
- **Hardware Real (RPi + Hailo-8)** — câmara física capturada via `rpicam-vid` em formato YUV420, convertida para BGR. O modelo utilizado é o `.hef`, já compilado e otimizado para o acelerador Hailo-8.

## Etapa 2 — Inferência

O frame capturado é processado pelo modelo de deteção. O fluxo varia consoante o ambiente:

- **`.pt` (PyTorch / CARLA)** — o frame vai direto para o modelo via Ultralytics (`model.predict()`), que trata internamente a inferência, decodificação, NMS e extração de máscaras.
- **`.hef` (Hailo-8 / RPi)** — o frame é pré-processado (redimensionado, convertido BGR→RGB) e enviado para o NPU via `HailoEngine.infer()`, que devolve tensores crus.

## Etapa 3 — Pós-processamento dos Tensores (apenas `.hef`)

Esta etapa aplica-se apenas ao `.hef`, pois o Ultralytics (`.pt`) trata internamente a decodificação, NMS e extração de máscaras. No `.hef`, o Hailo devolve tensores crus que precisam de ser interpretados manualmente através de dois passos:

- **`YoloSegDecoder`** — descobre a topologia de saída do modelo, multiplica os coeficientes de máscara pelos tensores protótipo, aplica threshold de confiança e devolve uma máscara binária `uint8`.
- **`MaskFilters`** — limpa a máscara com operações morfológicas (MORPH_CLOSE + MORPH_OPEN) para preencher gaps em tracejados e remover ruído isolado.

## Etapa 4 — BEV Transform (Bird's Eye View)

BEV é a vista de cima da estrada. Esta etapa é necessária pois numa imagem frontal as faixas aparentam convergir ao longe devido à perspetiva, tornando impossível medir distâncias reais e calcular o CTE com precisão. Ao transformar a imagem para uma vista top-down, as faixas ficam paralelas e os píxeis passam a ter uma relação direta com metros reais, permitindo ao Sliding Windows funcionar com precisão.

Para que esta transformação seja possível, é necessária uma **calibração prévia** — definir 4 pontos (`src_points`) sobre a estrada no frame frontal que formam um trapézio, e o retângulo correspondente na BEV (`dst_points`). Esta calibração é feita com a ferramenta `calibrar.py` e depende da posição física da câmara — se a câmara mudar de posição, é necessário recalibrar.

A transformação é aplicada via `cv2.getPerspectiveTransform` (`BEVTransform.warp()`).

## Etapa 5 — Sliding Windows + Polyfit

Com a imagem BEV, o algoritmo localiza as faixas esquerda e direita através de três passos: histograma para encontrar as bases das faixas na metade inferior da imagem, 9 janelas deslizantes que sobem de baixo para cima seguindo os píxeis de cada faixa, e ajuste de um polinómio de 2º grau (`x = ay² + by + c`) a cada faixa com os píxeis recolhidos.

## Etapa 6 — CTE (Cross-Track Error)

O CTE (Cross-Track Error) é o erro lateral normalizado `[-1, 1]` que representa o desvio do veículo em relação ao centro da faixa. É calculado avaliando os dois polinómios na base da imagem para obter a posição `x` de cada faixa, calculando o centro entre elas e comparando com o centro do veículo (meio da imagem). A diferença é normalizada pela largura da faixa — `0` significa veículo centrado, valores negativos indicam desvio para a esquerda e valores positivos desvio para a direita.

## Etapa 7 — PID (Controlador de Steering)

O PID recebe o CTE e calcula o ângulo de correção do steering. É composto por três componentes:

- **P (Proporcional)** — reage ao erro atual. Se o CTE é grande, corrige muito. Se é pequeno, corrige pouco.
- **I (Integral)** — corrige erros acumulados ao longo do tempo. Evita que o veículo fique sistematicamente desviado para um lado.
- **D (Derivativo)** — suaviza a correção prevendo a tendência do erro. Evita oscilações bruscas do volante.

O resultado é um valor de steering normalizado `[-1, 1]`. Os ganhos utilizados no projeto são `kp=1.2`, `ki=0.4`, `kd=0.35`.

## Etapa 8 — CAN Bus

O CAN Bus (Controller Area Network) é um protocolo de comunicação veicular que liga os componentes eletrónicos do carro. O `CanSender` recebe o valor de steering calculado pelo PID e envia-o pelo barramento CAN para o endereço `0x110`. O componente de controlo do servo recebe esse comando e aplica a correção física no veículo — é a ponte entre o software Python no RPi e o hardware físico do PiRacer.

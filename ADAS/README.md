# ADAS — Autonomous Driving Assistance System

Este diretório contém todos os módulos de desenvolvimento do sistema ADAS do projeto Team5 SennaTech, desde a validação em simulador até ao pipeline modular para hardware real (Raspberry Pi 5 + Hailo-8).

## Estrutura

### `CARLA-Simulator/`
Ambiente virtual de loop fechado (CARLA 0.9.16) usado para:
- Gerar o dataset de treino (pares imagem RGB + máscara binária de faixas)
- Comparar arquiteturas YOLO em simultâneo.
- Validar o pipeline LKA + PID (20Hz, CTE normalizado) antes de qualquer conversao .pt para .hef e deploy no hardware real

> Documentação detalhada: [`CARLA-Simulator/README.md`](CARLA-Simulator/README.md), [`CARLA-First-Pass`](../docs/CARLA-Simulator/README.md)

### `convert_hailo/`
Pipeline de conversão de modelos YOLO (`.pt` → ONNX → `.hef`) para deployment no acelerador Hailo-8. Suporta o fluxo via Hailo Model Zoo (YOLOv8-seg) e fluxo BYOM para modelos custom (YOLO26-seg).

> Documentação detalhada: [`convert_hailo/README.md`](convert_hailo/README.md)

### `LKA/`
Pipeline de referência em PyTorch para deteção de faixas e cálculo de erro lateral (CTE). Recebe um frame RGB e devolve `cte_normalized [-1, 1]` para o controlador PID, através de: inferência YOLO-seg → limpeza morfológica → transformação BEV → Sliding Windows + Polyfit. Inclui ferramenta de calibração BEV interativa e scripts de teste offline (imagem, vídeo, webcam).

> Modelos treinados disponíveis em `LKA_trained_models/` — modelo de produção: `yolov26sseg_cltusm_v1.pt`

### `Object_Detection/`
Módulo de deteção de objetos a correr em produção no Hailo-8. Carrega um modelo `.hef` (YOLO26n), lê frames da câmara via `rpicam-vid` e executa pós-processamento manual (decode 3 escalas + NMS) para detetar 13 classes custom: sinais de velocidade, semáforos, stop, crosswalk, obstáculos e carros. Display via GStreamer `waylandsink`.

> Modelos compilados disponíveis em `models/`: `yolo26n_v1.hef`, `yolo26n_v2.hef`

### `pipeline/`
Pipeline de produção LFA (Lane Following Assist) a correr no RPi + Hailo-8. Arquitetura em camadas: inferência `.hef` no NPU → decoder YOLO-seg → filtros morfológicos → BEV → Sliding Windows → LaneIdentityTracker (EMA + prevenção de swap de faixas) → PID → CAN bus. Suporta Virtual Lanes (estima faixa em falta com base na largura calibrada) e modo `--remote` para stream via stdout.

> Documentação detalhada: [`pipeline/README.md`](pipeline/README.md)

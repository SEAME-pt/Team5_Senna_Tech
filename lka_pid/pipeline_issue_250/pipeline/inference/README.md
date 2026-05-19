# Inference Module

## Index
- [Overview](#overview)
- [Hardware](#hardware)
- [Hailo Platform](#hailo-platform)
- [API / Methods](#api--methods)
- [Data Contract](#data-contract)
- [Execution Flow](#execution-flow)
- [Notes](#notes)

## Overview
Executa os modelos no acelerador Hailo-8 e devolve os tensores crus para as etapas seguintes da pipeline.

Inicialmente, a implementação da inferência estava dentro de `core/hailo_engine.py`. Durante a reestruturação da pipeline, o nome foi revisto porque `core` comunica a ideia de utilitários centrais e contratos compartilhados, enquanto a inferência é uma etapa funcional concreta do fluxo de execução.

Por esse motivo, a responsabilidade passou a ser representada pelo módulo `inference/`.

## Hardware
- **Acelerador:** Hailo-8 NPU
- **Modelos:** `yolo26n_seg_640.hef` (LKA), `yolo26n_v4.hef` (Object Detection)

## Hailo Platform
O módulo de inferência utiliza componentes da biblioteca `hailo_platform`, que é a SDK responsável por disponibilizar acesso ao acelerador Hailo-8 e à execução de modelos compilados no formato `.hef`.

Esses imports não pertencem à lógica de domínio da pipeline. Eles fazem parte da infraestrutura necessária para carregar o modelo, configurar o dispositivo e executar a inferência no hardware.

**`HEF`**
Responsável por carregar o arquivo `.hef`, que contém o modelo já compilado para execução na Hailo.

**`VDevice`**
Representa o dispositivo virtual de inferência. É a abstração usada pela SDK para disponibilizar acesso ao hardware Hailo e permitir que os modelos sejam configurados e executados.

**`ConfigureParams`**
Responsável por criar os parâmetros de configuração usados no carregamento do modelo para o dispositivo.

**`HailoStreamInterface`**
Define a interface de comunicação usada entre o sistema e o dispositivo Hailo. No caso atual, a inferência é configurada para usar `PCIe`.

**`InputVStreamParams`**
Responsável por configurar os parâmetros do stream de entrada da rede, ou seja, como os dados de entrada serão enviados para o modelo.

**`OutputVStreamParams`**
Responsável por configurar os parâmetros dos streams de saída, definindo como os resultados da inferência serão lidos.

**`InferVStreams`**
Cria o pipeline de inferência usado para enviar inputs ao modelo e receber os outputs gerados pela rede.

**`FormatType`**
Define o formato dos dados de saída. No contexto atual, os outputs são configurados como `FLOAT32`, o que facilita o pós-processamento no Python.

## API / Methods

### `HailoEngine.__init__(hef_path, target, debug=False)`
Carrega o modelo `.hef`, prepara os metadados de entrada e guarda as dependências necessárias para configurar a inferência.

#### Parâmetros
- `hef_path` aponta para o ficheiro `.hef` que será executado.
- `target` é o `VDevice` ou recurso equivalente que fornece acesso ao hardware Hailo.
- `debug` ativa logs adicionais de carregamento, pré-processamento e saída.

#### Efeitos
- Instancia `HEF(hef_path)`.
- Lê a primeira `input_vstream_info` para obter o nome de entrada.
- Inicializa os campos internos usados pelo contexto e pela execução.

### `HailoEngine.preprocess(img_rgb)`
Prepara um frame RGB para entrada na rede.

#### Comportamento
- Redimensiona o frame para `self.net_size`.
- Adiciona dimensão de batch.
- Converte o array para `uint8`.

#### Saída
- `numpy.ndarray` com shape `(1, net_size, net_size, 3)`.

#### Observações
- O método assume entrada em RGB.
- Os logs de debug mostram shape original, shape redimensionado e dtype final.

### `HailoEngine.__enter__()`
Configura o modelo no dispositivo Hailo e prepara o pipeline de inferência.

#### Comportamento
- Cria os parâmetros de configuração via `ConfigureParams.create_from_hef`.
- Configura o `target` com o `.hef`.
- Cria os parâmetros de stream de entrada e saída.
- Instancia `InferVStreams` e abre o contexto interno do pipeline.
- Atualiza `self.input_name` com a chave efetiva do stream de entrada.

#### Efeitos
- Deixa o engine pronto para receber chamadas a `infer()`.
- Retorna a própria instância para uso com `with`.

### `HailoEngine.infer(img_rgb)`
Executa uma inferência completa para um frame RGB.

#### Comportamento
- Chama `preprocess(img_rgb)`.
- Ativa o grupo de rede com `self._ng.activate(...)`.
- Envia o input ao `InferVStreams`.
- Retorna o dicionário de outputs crus da rede.

#### Saída
- `dict` com os tensores produzidos pelo modelo.

#### Observações
- Em modo debug, loga as chaves e os shapes dos outputs.
- O método depende de `__enter__` já ter sido executado.

### `HailoEngine.__exit__(exc_type, exc_val, exc_tb)`
Fecha o pipeline de inferência e liberta os recursos associados ao contexto.

#### Comportamento
- Emite log de encerramento em debug.
- Finaliza `self.pipeline` se ele existir.

#### Efeitos
- Liberta o contexto aberto pelo `with`.
- Evita deixar streams da Hailo abertos após a execução.

## Data Contract
| Campo | Tipo | Shape |
|---|---|---|
| `rgb` | `numpy.ndarray uint8` | `(H, W, 3)` |

## Output
| Campo | Tipo | Descrição |
|---|---|---|
| `outputs_lane` | `dict` | 4 tensores crus do modelo LKA |
| `outputs_obj` | `dict` | 6 tensores crus do modelo Object Detection |

## Execution Flow
Antes da inferência, o módulo executa:

- `resize` para o tamanho esperado pela rede;
- adição da dimensão de batch;
- conversão final para `uint8`.

Na `main2`, a câmera já entrega frames em `RGB`, portanto o módulo de inferência não precisa mais converter `BGR -> RGB`. Esse comportamento foi removido para manter o contrato entre módulos simples e coerente.

Esse comportamento fica encapsulado no módulo de inferência para que a `main` funcione apenas como orquestradora.

## Papel na `main2`
Na `main2`, a inferência está a ser integrada como a etapa imediatamente a seguir à câmera. O objetivo desta fase é validar o fluxo `camera -> inference` antes de acoplar decoder, geometria e controlo.

Nesta fase da reestruturação, a `main2` já prepara os dois modelos da pipeline:

- um `HailoEngine` para lane detection;
- um `HailoEngine` para object detection.

Ambos são inicializados antes da abertura da câmera e compartilham o mesmo `VDevice`.

## Ordem de inicialização na execução
Embora a câmera seja a primeira etapa do fluxo de dados da pipeline, a infraestrutura da inferência pode ser inicializada antes dela durante a execução do sistema.

Essa ordem de inicialização faz sentido porque o `VDevice` e o `HailoEngine` precisam estar prontos antes que a câmera comece a produzir frames continuamente. Dessa forma, o sistema evita iniciar a captura sem ter a etapa seguinte preparada para consumir os dados.

Na prática, a distinção é a seguinte:

- ordem do fluxo de dados: `camera -> inference -> post_processing -> ...`
- ordem de inicialização dos recursos: `VDevice -> HailoEngine(lane) -> HailoEngine(object) -> Camera -> loop`

Essa separação melhora a robustez da aplicação e permite falhar cedo caso exista algum problema com o hardware Hailo ou com o carregamento do modelo `.hef`.

## Notes
- O módulo utiliza `VDevice` da Hailo para partilhar o dispositivo entre múltiplos engines quando necessário.
- A `main2` já recebe dois caminhos `.hef`, um para lane detection e outro para object detection.
- Nesta etapa, os engines já são inicializados na `main2`, mesmo antes de a inferência por frame ser ligada ao loop principal.

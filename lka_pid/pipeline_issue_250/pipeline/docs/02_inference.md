# 02 — Inference

## Responsabilidade
Executa os modelos no acelerador Hailo-8 e devolve os tensores crus para as etapas seguintes da pipeline.

## Justificativa da mudança de nome
Inicialmente, a implementação da inferência estava dentro de `core/hailo_engine.py`. Durante a reestruturação da pipeline, o nome foi revisto porque `core` comunica a ideia de utilitários centrais e contratos compartilhados, enquanto a inferência é uma etapa funcional concreta do fluxo de execução.

Por esse motivo, a responsabilidade passou a ser representada pelo módulo `inference/`. Essa mudança melhora a clareza arquitetural da pipeline e deixa mais explícita a sequência:

1. `camera`
2. `inference`
3. `post_processing`
4. `LFA`
5. `decision`
6. `external interfaces`

Assim, o nome do módulo passa a refletir melhor o seu papel dentro da arquitetura, em vez de o tratar como infraestrutura genérica.

## Hardware
- **Acelerador:** Hailo-8 NPU
- **Modelos:** `yolo26n_seg_640.hef` (LKA), `yolo26n_v4.hef` (Object Detection)

## Dependências da Hailo Platform

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

## Papel do `VDevice`

`VDevice` é a abstração da SDK da Hailo que representa o dispositivo virtual de inferência. Ele é responsável por disponibilizar acesso ao acelerador Hailo para que os modelos `.hef` possam ser configurados e executados.

Na arquitetura da pipeline, o `VDevice` pertence à camada de infraestrutura da inferência. Ele não contém lógica de negócio, não processa frames diretamente e não interpreta resultados do modelo. Sua função é apenas disponibilizar o hardware para uso pelo módulo de inferência.

Na `main2`, o `VDevice` deve ser inicializado antes do `HailoEngine`, porque o engine depende dele para carregar e executar o modelo. Por isso, ele aparece no fluxo de inicialização com `with`, garantindo que o acesso ao hardware seja aberto no início da execução e liberado corretamente no final.

O `VDevice` é passado como argumento para o `HailoEngine` para que a `main2` mantenha o controlo do ciclo de vida dos recursos da inferência, enquanto o módulo `inference` fica responsável apenas pela execução do modelo.

Na estrutura atual da `main2`, um único `VDevice` é inicializado e compartilhado por dois `HailoEngine`: um para o modelo de lane detection e outro para o modelo de object detection.

## Papel arquitetural desses imports

Do ponto de vista arquitetural, esses elementos pertencem à camada de infraestrutura da inferência. Eles existem para permitir que o módulo `inference` se comunique com a SDK da Hailo e execute o modelo no acelerador.

A `main2` não deve conhecer esses detalhes diretamente. O objetivo é que a `main2` apenas inicialize o módulo de inferência e consuma sua interface, enquanto o `HailoEngine` encapsula toda a complexidade de integração com a `hailo_platform`.

## Input
| Campo | Tipo | Shape |
|---|---|---|
| `rgb` | `numpy.ndarray uint8` | `(H, W, 3)` |

## Output
| Campo | Tipo | Descrição |
|---|---|---|
| `outputs_lane` | `dict` | 4 tensores crus do modelo LKA |
| `outputs_obj` | `dict` | 6 tensores crus do modelo Object Detection |

## Pré-processamento interno
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

## Observações
- O módulo utiliza `VDevice` da Hailo para partilhar o dispositivo entre múltiplos engines quando necessário.
- A `main2` já recebe dois caminhos `.hef`, um para lane detection e outro para object detection.
- Nesta etapa, os engines já são inicializados na `main2`, mesmo antes de a inferência por frame ser ligada ao loop principal.

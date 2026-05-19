# Lane Post-Processing

## Index
- [Overview](#overview)
- [Module](#module)
- [Data Contract](#data-contract)
- [Notes](#notes)

## Overview
Trata os outputs crus do modelo de lane segmentation e converte-os em uma máscara binária limpa das faixas.

## Module
`lane_post_processing.py` concentra as duas classes desta etapa:
- `YoloSegDecoder`
- `MaskFilters`

### `YoloSegDecoder`
Responsável por identificar o formato dos tensores do modelo de segmentação e reconstruir a máscara das faixas.

#### `__init__(score_threshold=0.25, top_k=200)`
Define os limiares usados para selecionar candidatos e limitar o número de máscaras consideradas.

**Parâmetros**
- `score_threshold` define o limiar mínimo para manter uma proposta de máscara.
- `top_k` limita o número de candidatos considerados na reconstrução.

**Efeitos**
- Guarda os limiares que serão usados em `decode_to_mask`.

#### `decode_to_mask(outputs, orig_h, orig_w)`
Recebe os tensores crus da inferência e devolve uma máscara binária da estrada/faixas.

**Comportamento**
- Identifica automaticamente o formato dos tensores de saída.
- Reconstrói a máscara usando proto features e coeficientes de máscara.
- Aplica seleção por score e threshold de confiança.
- Redimensiona o resultado final para a resolução original do frame.

**Entradas**
- `outputs`: dicionário com os tensores crus do modelo.
- `orig_h` e `orig_w`: dimensões do frame original.

**Saída**
- `numpy.ndarray uint8` com a máscara binária da lane.

### `MaskFilters`
Responsável por limpar a máscara binária usando operações morfológicas.

#### `__init__(close_kernel=(5, 15), open_kernel=(5, 5))`
Configura os kernels morfológicos usados na limpeza da máscara.

**Parâmetros**
- `close_kernel` define o kernel do fechamento morfológico.
- `open_kernel` define o kernel da abertura morfológica.

**Efeitos**
- Cria kernels retangulares usados em `process`.

#### `process(mask)`
Aplica fechamento e abertura morfológica para reduzir ruído e preencher falhas.

**Comportamento**
- Executa `MORPH_CLOSE` para preencher buracos pequenos e unir regiões separadas.
- Executa `MORPH_OPEN` para remover ruído e artefactos isolados.

**Entrada**
- `mask`: máscara binária gerada pelo decoder.

**Saída**
- Máscara binária mais limpa e estável para a etapa de geometria.

## Data Contract
| Field | Type | Meaning |
|---|---|---|
| `outputs_lane` | `dict` | Tensores crus do modelo de lane segmentation |
| `binary_mask` | `numpy.ndarray uint8` | Máscara binária das faixas |

## Notes
- Esta camada é a ponte entre `inference` e `LFA`.
- Os detalhes de formato dos tensores ficam encapsulados aqui.

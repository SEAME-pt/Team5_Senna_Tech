# LFA Geometry

## Responsabilidade
Processa a máscara da faixa para extrair geometria útil ao controlo.

## Etapas
- `BEV Transform` - transforma a máscara para vista top-down
- `Sliding Windows` - localiza faixas e ajusta polinómios
- `CTE` - extrai o erro lateral normalizado

## Documentação Interna

### 04 - BEV Transform
Transforma a máscara binária de perspetiva frontal para vista top-down (`Bird's Eye View`), permitindo medir distâncias reais na estrada.

#### Módulo
- `BEVTransform` - transformação de perspetiva via `cv2.getPerspectiveTransform`

#### Input
| Campo | Tipo | Shape |
|---|---|---|
| `binary_mask` | `numpy.ndarray uint8` | `(H, W)` |

#### Output
| Campo | Tipo | Shape |
|---|---|---|
| `bev_mask` | `numpy.ndarray uint8` | `(H, W)` |

#### Observações
- Requer calibração prévia (`src_points` e `dst_points`)
- A preencher durante os testes

### 05 - Sliding Windows
Localiza as faixas esquerda e direita na imagem BEV e ajusta polinómios de 2º grau a cada uma.

#### Módulo
- `SlidingWindowsLaneFitter` - histograma + 9 janelas deslizantes + `polyfit`

#### Input
| Campo | Tipo | Shape |
|---|---|---|
| `bev_mask` | `numpy.ndarray uint8` | `(H, W)` |

#### Output
| Campo | Tipo | Descrição |
|---|---|---|
| `fit_result` | `LaneFitResult` | Polinómios left/right + CTE |
| `fit_result.left_fit` | `numpy.ndarray` ou `None` | Coeficientes do polinómio esquerdo |
| `fit_result.right_fit` | `numpy.ndarray` ou `None` | Coeficientes do polinómio direito |
| `fit_result.cte_norm` | `float` ou `None` | CTE normalizado `[-1, 1]` |

#### Observações
- A preencher durante os testes

### 06 - CTE
Extrai o erro lateral normalizado do resultado do Sliding Windows. Representa o desvio do veículo em relação ao centro da faixa.

#### Input
| Campo | Tipo | Descrição |
|---|---|---|
| `fit_result.cte_norm` | `float` ou `None` | CTE calculado pelo Sliding Windows |

#### Output
| Campo | Tipo | Descrição |
|---|---|---|
| `cte` | `float` | Erro lateral normalizado `[-1, 1]` |

#### Comportamento
- `0` - veículo centrado
- Negativo - desvio para a esquerda
- Positivo - desvio para a direita
- Se `cte_norm` for `None` (faixas não detetadas), fallback `0.0`

#### Observações
- A preencher durante os testes

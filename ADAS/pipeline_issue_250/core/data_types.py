"""
LaneFitResult Contém todos os dados resultantes da deteção e ajuste das faixas de rodagem.
 
Atributos:
left_fit:        Coeficientes [a, b, c] do polinómio de 2º grau para a faixa esquerda
                         (x = a*y² + b*y + c, onde y cresce para baixo)
right_fit:       Mesmo para a faixa direita
cte_pixels:      Erro lateral em píxeis (positivo = veículo à direita do centro)
cte_norm:        Erro lateral normalizado entre -1.0 e +1.0
curvature_px:    Raio de curvatura em píxeis (>10000 = reta)
left_found:      True se a faixa esquerda foi detetada (não é virtual)
right_found:     True se a faixa direita foi detetada (não é virtual)
debug_image:     Imagem de depuração com as janelas deslizantes (ou None)
left_is_virtual: True se a faixa esquerda foi estimada (não detetada diretamente)
right_is_virtual:True se a faixa direita foi estimada
swap_pending:    True se o tracker suspeita que as faixas foram trocadas
"""

from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class LaneFitResult:
    left_fit:        Optional[np.ndarray]
    right_fit:       Optional[np.ndarray]
    cte_pixels:      Optional[float]
    cte_norm:        Optional[float]
    curvature_px:    Optional[float]
    left_found:      bool
    right_found:     bool
    debug_image:     Optional[np.ndarray]
    left_is_virtual: bool = False
    right_is_virtual: bool = False
    swap_pending:    bool = False


"""
Identity tracker result: ensures that the left track
is always on the left and the right track is always on the right, frame by frame.
"""
@dataclass
class TrackedLaneFit:
    left_fit:         Optional[np.ndarray]
    right_fit:        Optional[np.ndarray]
    left_is_virtual:  bool = False
    right_is_virtual: bool = False
    swap_pending:     bool = False
"""
ObstacleTracker
---------------
Rastreia o obstáculo mais relevante no corredor frame a frame.
Calcula:
  - área relativa atual
  - delta de área entre frames (taxa de crescimento)
  - posição BEV normalizada (0=esquerda, 1=direita)
  - número de frames consecutivos no corredor

Com base nisso, classifica a situação em:
  - CLEAR      : sem obstáculo relevante no corredor
  - AVOIDANCE  : obstáculo detectado com antecedência (crescimento lento)
  - BRAKE      : obstáculo apareceu de repente (crescimento rápido)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from object.perception_objects import ClassID, ObstacleSituation

@dataclass
class ObstacleInfo:
    situation:          ObstacleSituation
    area:               float          # área relativa atual  [0, 1]
    delta_area:         float          # variação de área por frame
    bev_x_norm:         float          # posição BEV normalizada [0=esq, 1=dir]
    frames_in_corridor: int            # frames consecutivos no corredor
    side:               str            # "left" | "right" | "center"


class ObstacleTracker:
    """
    Parâmetros
    ----------
    area_brake_threshold   : se delta_area >= este valor num único frame → BRAKE
    area_avoidance_min     : área mínima para considerar avoidance
    frames_to_confirm      : frames consecutivos para confirmar avoidance
    frame_width_bev        : largura da imagem BEV em px (= CAM_WIDTH)
    """

    def __init__(
        self,
        area_brake_threshold:  float = 0.025,
        area_avoidance_min:    float = 0.010,
        frames_to_confirm:     int   = 4,
        frame_width_bev:       int   = 640,
    ):
        self.area_brake_threshold  = area_brake_threshold
        self.area_avoidance_min    = area_avoidance_min
        self.frames_to_confirm     = frames_to_confirm
        self.frame_width_bev       = frame_width_bev

        self._prev_area:         float = 0.0
        self._frames_in_corridor: int  = 0
        self._last_bev_x_norm:   float = 0.5

    # ------------------------------------------------------------------
    def update(self, detections_in_corridor: list) -> ObstacleInfo:
        """
        detections_in_corridor : lista de dicts com chaves
            "class_id"       (int)
            "relative_area"  (float)
            "debug_info"     (dict com "bev_x")
        Apenas ClassID.OBSTACLE (valor 8) é considerado.
        """
        from object.perception_objects import ClassID

        # Filtra só obstáculos no corredor
        obstacles = [
            d for d in detections_in_corridor
            if d.get("class_id") == ClassID.OBSTACLE.value
            and d.get("in_corridor", False)
        ]

        # Sem obstáculo → reset e retorna CLEAR
        if not obstacles:
            self._frames_in_corridor = 0
            self._prev_area          = 0.0
            return ObstacleInfo(
                situation          = ObstacleSituation.CLEAR,
                area               = 0.0,
                delta_area         = 0.0,
                bev_x_norm         = self._last_bev_x_norm,
                frames_in_corridor = 0,
                side               = "center",
            )

        # Pega o obstáculo de maior área (mais relevante)
        best = max(obstacles, key=lambda d: d.get("relative_area", 0.0))
        area     = best.get("relative_area", 0.0)
        debug    = best.get("debug_info", {})
        bev_x    = debug.get("bev_x", self.frame_width_bev * 0.5)
        bev_x_norm = float(bev_x) / float(self.frame_width_bev)
        bev_x_norm = max(0.0, min(1.0, bev_x_norm))

        if self._frames_in_corridor == 0:
            delta_area = 0.0 # Primeiro frame a ver o objeto, não há delta real
        else:
            delta_area = area - self._prev_area

        self._prev_area          = area
        self._last_bev_x_norm    = bev_x_norm
        self._frames_in_corridor += 1

        # Determina o lado do obstáculo relativamente ao centro (0.5)
        if bev_x_norm < 0.43:
            side = "left"
        elif bev_x_norm > 0.57:
            side = "right"
        else:
            side = "center"

        # ── Classificação ──────────────────────────────────────────────
        # BRAKE: crescimento muito rápido num único frame
        if delta_area >= self.area_brake_threshold:
            situation = ObstacleSituation.BRAKE

        # AVOIDANCE: área relevante E presente há frames suficientes
        elif (
            area >= self.area_avoidance_min
            and self._frames_in_corridor >= self.frames_to_confirm
        ):
            situation = ObstacleSituation.AVOIDANCE

        # Ainda acumulando frames de confirmação
        else:
            situation = ObstacleSituation.CLEAR

        return ObstacleInfo(
            situation          = situation,
            area               = area,
            delta_area         = delta_area,
            bev_x_norm         = bev_x_norm,
            frames_in_corridor = self._frames_in_corridor,
            side               = side,
        )

    def reset(self):
        self._prev_area          = 0.0
        self._frames_in_corridor = 0

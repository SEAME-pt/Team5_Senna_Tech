"""
Responsabilidades:
  1. Calcular o CTE alvo com base no estado da FSM
       - Estados de desvio (PREPARE_AVOID, AVOIDING, BLIND_WAIT) → CTE deslocado
         para o lado OPOSTO ao obstáculo (determinado pelo ObstacleTracker)
       - Estado RETURNING → interpola suavemente de CTE deslocado → 0.0
       - Restantes estados → CTE = 0.0 (centro da faixa)

  2. Gerir o timer de BLIND_WAIT com time.time() (mais correto que frames,
     pois é independente de variações de FPS)

  3. Confirmar quando a interpolação de retorno está completa
     (sinal para a FSM transitar RETURNING → estado de velocidade anterior)

Parâmetros
----------
lane_offset       : magnitude do desvio normalizado [0, 1].
                    170 px de faixa → 65 px ≈ 0.38 normalizado.
blind_wait_time   : segundos a aguardar em BLIND_WAIT antes de retornar.
return_duration_s : duração da interpolação de retorno ao centro.
"""

import time


class PathPlanner:

    def __init__(
        self,
        lane_offset:       float = 0.38,
        blind_wait_time:   float = 2.5,
        return_duration_s: float = 1.5,
    ):
        self.lane_offset       = lane_offset
        self.blind_wait_time   = blind_wait_time
        self.return_duration_s = return_duration_s

        # Timer de blind wait
        self._blind_timer_start: float | None = None

        # Estado de interpolação de retorno
        self._returning:       bool  = False
        self._return_start:    float = 0.0
        self._cte_at_return:   float = 0.0

        # Lado do desvio actual ("left" | "right")
        self._desvio_side: str = "left"

    # ──────────────────────────────────────────────────────────────
    def calculate_target_cte(
        self,
        current_state,
        obstacle_side: str = "right",   # "left" | "right" | "center"
    ) -> float:
        """
        Retorna o CTE alvo a passar ao PID neste frame.

        current_state : State da FSM
        obstacle_side : lado do obstáculo em BEV (do ObstacleTracker)
        """
        from decision.decision_fsm import State

        # ── Desvio ativo ──────────────────────────────────────────
        if current_state in (
            State.PREPARE_AVOID,
            State.AVOIDING,
            State.BLIND_WAIT,
        ):
            self._returning = False  # cancela qualquer retorno anterior

            # Desviar para o lado oposto ao obstáculo
            if obstacle_side in ("right", "center"):
                self._desvio_side = "left"
                return -self.lane_offset        # CTE negativo = virar à esquerda
            else:
                self._desvio_side = "right"
                return +self.lane_offset        # CTE positivo = virar à direita

        # ── Retorno interpolado ────────────────────────────────────
        if current_state == State.RETURNING:
            if not self._returning:
                self._returning    = True
                self._return_start = time.perf_counter()
                # CTE de partida = posição deslocada
                self._cte_at_return = (
                    -self.lane_offset
                    if self._desvio_side == "left"
                    else +self.lane_offset
                )

            elapsed  = time.perf_counter() - self._return_start
            progress = min(1.0, elapsed / self.return_duration_s)
            return _lerp(self._cte_at_return, 0.0, progress)

        # ── Condução normal ────────────────────────────────────────
        self._returning = False
        return 0.0

    # ──────────────────────────────────────────────────────────────
    def check_blind_wait_timeout(self) -> bool:
        """
        Deve ser chamado a cada frame quando a FSM está em BLIND_WAIT.
        Inicia o timer na primeira chamada; retorna True quando expirou.
        """
        if self._blind_timer_start is None:
            self._blind_timer_start = time.time()
            return False
        return (time.time() - self._blind_timer_start) >= self.blind_wait_time

    def reset_blind_timer(self):
        """Chamado quando a FSM sai de BLIND_WAIT (para qualquer estado)."""
        self._blind_timer_start = None

    # ──────────────────────────────────────────────────────────────
    def return_complete(self) -> bool:
        """True quando a interpolação de retorno terminou."""
        if not self._returning:
            return False
        elapsed = time.perf_counter() - self._return_start
        return elapsed >= self.return_duration_s

    def reset(self):
        """Reset completo (usado após EMERGENCY ou reinício de manobra)."""
        self._blind_timer_start = None
        self._returning         = False
        self._return_start      = 0.0
        self._cte_at_return     = 0.0


# ── helpers ────────────────────────────────────────────────────────────

def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

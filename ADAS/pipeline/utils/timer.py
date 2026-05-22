import time
from collections import deque

_FPS_WINDOW = 30  # frames for sliding window average

class Timer:
    def __init__(self):
        self._start_times = {}
        self._durations = {}
        self._loop_start = None
        self._loop_duration_ms = 0.0
        self._frame_times = deque(maxlen=_FPS_WINDOW)

    def start_loop(self):
        self._loop_start = time.perf_counter()

    def end_loop(self):
        """Finaliza o loop e regista a duração real. Chamar no fim de cada iteração."""
        if self._loop_start is None:
            return
        self._loop_duration_ms = (time.perf_counter() - self._loop_start) * 1000
        self._frame_times.append(self._loop_duration_ms)

    def get_loop_duration(self):
        """Duração do loop actual em ms (calculada em end_loop)."""
        return self._loop_duration_ms

    def start_stage(self, stage_name):
        self._start_times[stage_name] = time.perf_counter()

    def end_stage(self, stage_name):
        start = self._start_times.get(stage_name, time.perf_counter())
        duration = (time.perf_counter() - start) * 1000
        self._durations[stage_name] = duration
        return duration

    def get_fps(self):
        """FPS médio sobre os últimos frames (janela deslizante)."""
        if not self._frame_times:
            return 0.0
        avg_ms = sum(self._frame_times) / len(self._frame_times)
        return 1000.0 / avg_ms if avg_ms > 0 else 0.0

    def get_report(self):
        return " | ".join([f"{k}: {v:.1f}ms" for k, v in self._durations.items()])

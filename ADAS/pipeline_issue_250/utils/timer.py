import time

class Timer:
    def __init__(self):
        """Initializes the timer with internal start times for stages and frames."""
        self._start_times = {}
        self._durations = {}
        self._loop_start = None
        self._last_frame_time = time.perf_counter()

    def start_loop(self):
        """Starts the timer for the main loop cycle."""
        self._loop_start = time.perf_counter()

    def get_loop_duration(self):
        """Returns elapsed time since start_loop in ms."""
        if self._loop_start is None:
            return 0.0
        return (time.perf_counter() - self._loop_start) * 1000

    def start_stage(self, stage_name):
        """Starts timing a specific pipeline stage."""
        self._start_times[stage_name] = time.perf_counter()

    def end_stage(self, stage_name):
        """Ends timing a stage and returns duration in ms."""
        start = self._start_times.get(stage_name, time.perf_counter())
        duration = (time.perf_counter() - start) * 1000
        self._durations[stage_name] = duration
        return duration

    def get_fps(self):
        """Calculates instantaneous FPS based on elapsed time since last call."""
        now = time.perf_counter()
        dt = now - self._last_frame_time
        self._last_frame_time = now
        return 1.0 / dt if dt > 0 else 0.0

    def get_report(self):
        """Returns a formatted string of all tracked stage timings."""
        return " | ".join([f"{k}: {v:.1f}ms" for k, v in self._durations.items()])

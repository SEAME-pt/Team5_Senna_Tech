import os

class HardwareMonitor:
    def __init__(self):
        # Inicializa o estado da CPU no momento em que a classe é instanciada
        self._cpu_stat_prev = self._read_cpu_stat()

    def _read_cpu_stat(self):
        """Lê o arquivo /proc/stat e retorna (user, system, idle, total) em jiffies."""
        try:
            with open("/proc/stat") as f:
                r = f.readline().split()
                user   = int(r[1]) + int(r[2])  # user + nice
                system = int(r[3])
                idle   = int(r[4])
                total  = sum(int(x) for x in r[1:])
                return user, system, idle, total
        except Exception:
            # Fallback caso não esteja em um sistema Linux compatível
            return 0, 0, 0, 1 

    def read_temp(self):
        """Lê a temperatura da CPU em graus Celsius."""
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as f:
                return int(f.read().strip()) / 1000.0
        except Exception:
            # Fallback caso o sensor não seja encontrado
            return 0.0

    def get_cpu_usage(self):
        """Calcula e retorna a porcentagem de CPU usada e livre desde a última chamada."""
        user_now, sys_now, idle_now, total_now = self._read_cpu_stat()
        user_prev, sys_prev, idle_prev, total_prev = self._cpu_stat_prev
        
        d_total  = total_now - total_prev
        d_user   = user_now  - user_prev
        d_sys    = sys_now   - sys_prev
        d_idle   = idle_now  - idle_prev
        
        cpu_pct_user   = d_user  / d_total * 100 if d_total > 0 else 0.0
        cpu_pct_sys    = d_sys   / d_total * 100 if d_total > 0 else 0.0
        cpu_pct_idle   = d_idle  / d_total * 100 if d_total > 0 else 0.0
        
        cpu_used = cpu_pct_user + cpu_pct_sys
        cpu_free = cpu_pct_idle
        
        # Atualiza o estado anterior para a próxima leitura
        self._cpu_stat_prev = (user_now, sys_now, idle_now, total_now)
        
        return cpu_used, cpu_free
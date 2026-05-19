#include "pid.h"

float absf_local(float value)
{
    return (value < 0.0f) ? -value : value;
}

float clamp_symmetric(float value, float limit)
{
    if (limit <= 0.0f)
        return 0.0f;
    if (value > limit)
        return limit;
    if (value < -limit)
        return -limit;
    return value;
}

float get_throttle_current_normalized(void)
{
    float speed_abs_kmh;

    tx_mutex_get(&g_speed_mutex, TX_WAIT_FOREVER);
    speed_abs_kmh = speed_kmh;
    tx_mutex_put(&g_speed_mutex);

    return clamp_symmetric(speed_abs_kmh / 10.0f, 1.0f);
}

float pidThrottleCalculation(pid_t *throttle_pid, float throttle_target, float dt)
{
    float current = get_throttle_current_normalized();
    if (throttle_target < 0.0f)
        current = -current;

    float throttle_cmd = pid_update(throttle_pid, throttle_target, current, dt);

    if (throttle_target == 0.0f)
    {
        pid_reset(throttle_pid);
        throttle_cmd = 0.0f;
    }

    return throttle_cmd;
}

float get_delta_time_seconds(ULONG *last_tick)
{
    ULONG now_tick = tx_time_get();
    ULONG elapsed_ticks = now_tick - *last_tick;

    if (elapsed_ticks == 0U)
        return 0.0f;

    *last_tick = now_tick;

    return (float)elapsed_ticks / (float)TX_TIMER_TICKS_PER_SECOND;
}

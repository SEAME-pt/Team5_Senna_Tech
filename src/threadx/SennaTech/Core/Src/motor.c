#include "can_manager.h"
#include "car.h"
#include "pid.h"
#include <inttypes.h>

static float clamp_symmetric_f(float value, float limit)
{
    if (limit <= 0.0f)
        return 0.0f;
    if (value > limit)
        return limit;
    if (value < -limit)
        return -limit;
    return value;
}

static float get_throttle_current_normalized(void)
{
    float speed_abs_kmh;

    tx_mutex_get(&g_speed_mutex, TX_WAIT_FOREVER);
    speed_abs_kmh = speed_kmh;
    tx_mutex_put(&g_speed_mutex);

    return clamp_symmetric_f(speed_abs_kmh / 10.0f, 1.0f);
}

float percent_from_can_int16(uint8_t low_byte, uint8_t high_byte)
{
    // Intel (little endian)
    uint16_t u_combined = ((uint16_t)high_byte << 8) | low_byte;

    int16_t raw = (int16_t)u_combined;

    float percent = raw * 0.01f;

    // safety clamp
    if (percent > 1.0f)  percent = 1.0f;
    if (percent < -1.0f) percent = -1.0f;

    return percent;
}

static float get_delta_time_seconds(ULONG *last_tick)
{
    ULONG now_tick = tx_time_get();
    ULONG elapsed_ticks = now_tick - *last_tick;

    if (elapsed_ticks == 0U)
        return 0.0f;

    *last_tick = now_tick;

    return (float)elapsed_ticks / (float)TX_TIMER_TICKS_PER_SECOND;
}

static float pidCalculation(pid_t *throttle_pid, float throttle_target, float dt)
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

    return throttle_cmd * 100.0f;
}

void motors_thread_entry(ULONG thread_input)
{
    uart_send("Motor Thread Entry\r\n");

    CAN_Frame frame;

    car_t car;
    car_init(&car, &hi2c1);

    pid_t throttle_pid;
    pid_init(&throttle_pid, 0.82f, 1.11f, 0.01f);
    pid_set_integral_limit(&throttle_pid, 0.70f);
    pid_set_output_limit(&throttle_pid, 1.0f);

    float throttle_target = 0.0f; // normalized [-1, 1]
    ULONG last_tick = tx_time_get();

    while (1)
    {
        if (tx_queue_receive(&g_rx_data_queue, &frame, THROTTLE_PERIOD_TICKS) == TX_SUCCESS)
        {
            if (frame.dlc < 2)
                continue;

            float percent = percent_from_can_int16(frame.data[0], frame.data[1]);

            if (frame.id == CAN_ID_MOTOR_CMD)
            {
                throttle_target = percent;
            }
            else if (frame.id == CAN_ID_STEER_CMD)
            {
                car_set_steering_percent(&car, percent);
            }
        }

        float dt = get_delta_time_seconds(&last_tick);
        if (dt <= 0.0f)
            continue;

        float throttle_cmd_percent = pidCalculation(&throttle_pid, throttle_target, dt);

        car_set_throttle_percent(&car, throttle_cmd_percent);
    }
}

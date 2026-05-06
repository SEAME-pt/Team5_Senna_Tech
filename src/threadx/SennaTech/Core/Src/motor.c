#include "can_manager.h"
#include "car.h"
#include "pid.h"
#include <inttypes.h>
#include <math.h>

static float get_throttle_current_normalized(void)
{
    float speed_abs_kmh;

    tx_mutex_get(&g_speed_mutex, TX_WAIT_FOREVER);
    speed_abs_kmh = speed_kmh;
    tx_mutex_put(&g_speed_mutex);

    return clamp_symmetric(speed_abs_kmh / 10.0f, 1.0f);
}

static float pidThrottleCalculation(pid_t *throttle_pid, float throttle_target, float dt)
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

static float get_delta_time_seconds(ULONG *last_tick)
{
    ULONG now_tick = tx_time_get();
    ULONG elapsed_ticks = now_tick - *last_tick;

    if (elapsed_ticks == 0U)
        return 0.0f;

    *last_tick = now_tick;

    return (float)elapsed_ticks / (float)TX_TIMER_TICKS_PER_SECOND;
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

static float steering_update(float target, float current, float dt)
{
    // Constants for controlling the adaptive smoothing algorithm behavior for steering
    // This algorithm prioritizes responsiveness in curves and stability in straights
    const float deadband = 0.03f;              // Deadband: ignores very small commands to avoid jitter
    const float direct_turn_threshold = 0.20f; // Threshold for large turns: apply direct change if target > 0.20 (slightly lowered for earlier turns)
    const float close_threshold = 0.02f;       // Proximity threshold: if delta < 0.02, snap to target
    const float minor_alpha = 0.25f;           // Low alpha for small corrections (slow smoothing, reduces oscillations)
    const float major_alpha = 0.65f;           // High alpha for medium corrections (faster smoothing)
    const float correction_alpha = 0.4f;       // Correction alpha (not currently used, reserved for future adjustments)

    // Apply deadband: if target is very small, treat as zero to avoid unnecessary movements
    if (fabsf(target) < deadband)
        target = 0.0f;

    // Calculate the difference between target and current value
    float delta = target - current;
    float abs_delta = fabsf(delta);

    // If very close to target, return target directly (avoids infinitesimal adjustments)
    if (abs_delta < close_threshold)
        return target;

    // For large changes (curves): apply directly for fast response
    // Condition: large target OR large delta (sudden change)
    if (fabsf(target) > direct_turn_threshold || abs_delta > 0.25f)
    {
        // Large curve changes should be applied quickly
        return clamp_symmetric(target, 1.0f);
    }

    // For medium corrections: use higher alpha for faster adjustment
    if (fabsf(target) > 0.10f)
        return clamp_symmetric(current + delta * major_alpha, 1.0f);

    // For small corrections: use lower alpha to smooth and reduce oscillations in straights
    return clamp_symmetric(current + delta * minor_alpha, 1.0f);
}

void motors_thread_entry(ULONG thread_input)
{
    uart_send("Motor Thread Entry\r\n");

    CAN_Frame frame;

    car_t car;
    car_init(&car, &hi2c1);

    pid_t throttle_pid;
    pid_init(&throttle_pid, 0.92f, 1.11f, 0.01f);
    pid_set_integral_limit(&throttle_pid, 0.70f);
    pid_set_output_limit(&throttle_pid, 1.0f);

    float throttle_target = 0.0f; // normalized [-1, 1]

    float steering_target = 0.0f; // normalized [-1, 1]
    float steering_current = 0.0f; // tracked servo position

    ULONG last_tick = tx_time_get();

    UINT mode = 1U; // 0 = autonomous, 1 = manual, 2 = debug
    uint8_t brake = 0;

    while (1)
    {
        if (tx_queue_receive(&g_rx_data_queue, &frame, THROTTLE_PERIOD_TICKS) == TX_SUCCESS)
        {
            float percent = -1;

            if (frame.dlc < 2)
                percent = frame.data[0];
            else
                percent = percent_from_can_int16(frame.data[0], frame.data[1]);

            if (frame.id == CAN_ID_MODE)
            {
                int16_t mode_cmd = (int16_t)(((uint16_t)frame.data[1] << 8) | frame.data[0]);

                if (mode_cmd == 0) {
                    uart_send("Switched to AUTO mode\r\n");
                    mode = 0;
                    pid_reset(&throttle_pid);
                    steering_current = steering_target;
                    last_tick = tx_time_get();
                }
                else if (mode_cmd == 1) {
                    uart_send("Switched to MANUAL mode\r\n");
                    mode = 1;
                    pid_reset(&throttle_pid);
                    steering_current = steering_target;
                    throttle_target = 0.0f;
                    steering_target = 0.0f;
                }
                else if (mode_cmd == 2) {
                    uart_send("Switched to DEBUG mode\r\n");
                    mode = 2;
                    pid_reset(&throttle_pid);
                    steering_current = steering_target;
                    throttle_target = 0.0f;
                    steering_target = 0.0f;
                }

                continue ;
            }

            if (frame.id == CAN_ID_STEER_CMD)
            {
                steering_target = percent;
                continue ;
            }

            if (frame.id == CAN_ID_ESTOP)
            {
                if (percent == 1 || percent == 5)
                {
                    throttle_target = 0.0f;
                    brake = 1;
                }
                else if (percent == 0)
                {
                    throttle_target = 0.07f;
                    brake = 0;
                }
                uart_send("percentage is: ");
                uart_send_int(percent);
                uart_send("\r\n");
                continue ;
            }
            if (frame.id == CAN_ID_MOTOR_CMD && (mode == 1U))
            {
                throttle_target = percent;
                continue ;
            }
            else if (frame.id == CAN_ID_MOTOR_CMD && mode == 2U)
            {
                throttle_target = 0.07f;
                continue ;
            }
        }

        float dt = get_delta_time_seconds(&last_tick);
        if (dt <= 0.0f)
            continue ;

        float throttle_cmd_percent = pidThrottleCalculation(&throttle_pid, throttle_target, dt);
        car_set_throttle_percent(&car, throttle_cmd_percent, brake);

        // Steering: use dynamic update to remove straight-line noise and speed up curves
        steering_current = steering_update(steering_target, steering_current, dt);
        car_set_steering_percent(&car, steering_current);
    }
}

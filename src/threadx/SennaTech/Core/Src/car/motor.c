#include "can_manager.h"
#include "car.h"
#include "pid.h"
#include <inttypes.h>
#include <math.h>

float decode_can_percent(uint8_t low_byte, uint8_t high_byte)
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

    ULONG last_tick = tx_time_get();

    UINT mode = 1U; // 0 = autonomous, 1 = manual, 2 = debug
    uint8_t brake = 0;

    float percent;

    while (1)
    {
        if (tx_queue_receive(&g_rx_data_queue, &frame, THROTTLE_PERIOD_TICKS) == TX_SUCCESS)
        {
            if (frame.dlc < 2)
                percent = frame.data[0];
            else
                percent = decode_can_percent(frame.data[0], frame.data[1]);

            if (frame.id == CAN_ID_MODE)
            {
                int16_t mode_cmd = (int16_t)(((uint16_t)frame.data[1] << 8) | frame.data[0]);

                if (mode_cmd == 0) {
                    uart_send("Switched to AUTO mode\r\n");
                    mode = 0;
                    pid_reset(&throttle_pid);
                    last_tick = tx_time_get();
                }
                else if (mode_cmd == 1) {
                    uart_send("Switched to MANUAL mode\r\n");
                    mode = 1;
                    pid_reset(&throttle_pid);
                    throttle_target = 0.0f;
                }
                else if (mode_cmd == 2) {
                    uart_send("Switched to DEBUG mode\r\n");
                    mode = 2;
                    pid_reset(&throttle_pid);
                    throttle_target = 0.0f;
                }

                continue ;
            }

            if (frame.id == CAN_ID_STEER_CMD)
            {
                steering_target = percent;
                continue ;
            }

            if (frame.id == CAN_ID_AI_MOVEMENT)
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

        car_set_steering_percent(&car, steering_target);
    }
}

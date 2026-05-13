#include "can_manager.h"
#include "car.h"
#include "pid.h"
#include <inttypes.h>
#include <math.h>

static e_car_mode get_car_mode(int16_t mode_cmd, ULONG *last_tick, float *throttle_target)
{
    if (mode_cmd == 0) 
    {
        uart_send("Switched to AUTO mode\r\n");
        *last_tick = tx_time_get();
        return MODE_AUTONOMOUS;
    }
    else if (mode_cmd == 1) 
    {
        uart_send("Switched to MANUAL mode\r\n");
        *throttle_target = 0.0f;
        return MODE_MANUAL;
    }
    else if (mode_cmd == 2) 
    {
        uart_send("Switched to DEBUG mode\r\n");
        *throttle_target = 0.0f;
        return MODE_DEBUG;
    }

    return MODE_MANUAL; // default
}

static float decode_can_percent(uint8_t low_byte, uint8_t high_byte)
{
    // Intel (little endian)
    uint16_t u_combined = ((uint16_t)high_byte << 8) | low_byte;
    int16_t raw = (int16_t)u_combined;

    if (raw == 200)
    {
        uart_send("EMERGENCY BRAKE\r\n");
        return 2.0f;
    }

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
    pid_init(&throttle_pid, 1.42f, 1.11f, 0.01f);
    pid_set_integral_limit(&throttle_pid, 0.70f);
    pid_set_output_limit(&throttle_pid, 1.0f);

    float throttle_target = 0.0f; // normalized [-1, 1]
    float steering_target = 0.0f; // normalized [-1, 1]

    ULONG last_tick = tx_time_get();
    
    e_car_mode mode = MODE_MANUAL;
    UINT brake = 0;

    float percent;

    while (1)
    {
        if (tx_queue_receive(&g_rx_data_queue, &frame, THROTTLE_PERIOD_TICKS) == TX_SUCCESS)
        {
            if (frame.dlc < 2)
                percent = frame.data[0];
            else
                percent = decode_can_percent(frame.data[0], frame.data[1]);

            // Mode switching
            if (frame.id == CAN_ID_MODE)
            {
                int16_t mode_cmd = (int16_t)(((uint16_t)frame.data[1] << 8) | frame.data[0]);

                mode = get_car_mode(mode_cmd, &last_tick, &throttle_target);
                pid_reset(&throttle_pid);
                continue ;
            }

            if (frame.id == CAN_ID_STEER_CMD)
            {
                steering_target = percent;
                continue ;
            }
    
            if (frame.id == CAN_ID_AI_MOVEMENT)
            {
                throttle_target = percent;
                uart_send("Received AI MOVEMENT command\r\n");
                uart_send_int(throttle_target * 100);
                uart_send("%\r\n");
                continue ;
            }
            else if (frame.id == CAN_ID_MOTOR_CMD && (mode == MODE_MANUAL))
                throttle_target = percent;

            else if (frame.id == CAN_ID_MOTOR_CMD && mode == MODE_DEBUG)
                throttle_target = 0.07f;

            continue ;
        }

        if (throttle_target == 2.0f) // Emergency brake
            brake = 1;
        else
            brake = 0;

        float dt = get_delta_time_seconds(&last_tick);
        if (dt <= 0.0f)
            continue ;

        float throttle_cmd_percent = pidThrottleCalculation(&throttle_pid, throttle_target, dt);

        car_set_throttle_percent(&car, throttle_cmd_percent, brake);
        car_set_steering_percent(&car, steering_target);
    }
}

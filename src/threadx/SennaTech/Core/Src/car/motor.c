#include "car_modes.h"

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

static void decode_drive_frame(CAN_Frame *frame, float *throttle_target, float *steering_target)
{
    int16_t throttle_raw = (int16_t)((uint16_t)frame->data[1] << 8 | frame->data[0]);
    int16_t steering_raw = (int16_t)((uint16_t)frame->data[3] << 8 | frame->data[2]);

    *throttle_target = throttle_raw * 0.01f;
    *steering_target = steering_raw * 0.01f;

    // safety clamp
    if (*throttle_target > 1.0f)  *throttle_target = 1.0f;
    if (*steering_target < -1.0f) *steering_target = -1.0f;
}

void motors_thread_entry(ULONG thread_input)
{
    uart_send("Motor Thread Entry\r\n");

    CAN_Frame frame;

    car_t car;
    car_init(&car, &hi2c1);

    pid_t throttle_pid;
    pid_init(&throttle_pid, 1.42f, 1.11f, 0.01f);

    // normalized [-1, 1]
    float throttle_target = 0.0f, steering_target = 0.0f;

    ULONG last_tick = tx_time_get();
    UINT brake = 0;
    e_car_mode mode = MODE_MANUAL;

    while (1)
    {
        if (tx_queue_receive(&g_rx_data_queue, &frame, THROTTLE_PERIOD_TICKS) == TX_SUCCESS)
        {
            // Mode switching
            if (frame.id == CAN_ID_MODE_MOVEMENT)
            {
                int16_t mode_cmd = (int16_t)frame.data[0];
                mode = get_car_mode(mode_cmd, &last_tick, &throttle_target);
                pid_reset(&throttle_pid);
                continue ;
            }
    
            if (frame.id == CAN_ID_AI_MOVEMENT && mode == MODE_AUTONOMOUS)
            {
                decode_drive_frame(&frame, &throttle_target, &steering_target);
                continue ;
            }
            else if (frame.id == CAN_ID_JOY_MOVEMENT)
            {
                if (mode == MODE_AUTONOMOUS)
                {
                    float joy_throttle, joy_steering;
                    decode_drive_frame(&frame, &joy_throttle, &joy_steering);

                    if (fabsf(joy_throttle) > 0.05f || fabsf(joy_steering) > 0.05f)
                    {
                        mode = MODE_MANUAL;
                        pid_reset(&throttle_pid);
                        throttle_target = joy_throttle;
                        steering_target = joy_steering;
                    }
                }
                else if (mode == MODE_MANUAL)
                    decode_drive_frame(&frame, &throttle_target, &steering_target);
                continue ;
            }

            if (frame.id == CAN_ID_MODE_PARKING)
            {
                uart_send("Entering PARKING mode\r\n");
                throttle_target = 2.0f; // Full brake
                steering_target = 0.0f;
                pid_reset(&throttle_pid);
                parking_mode_entry(&car, throttle_pid);
                continue ;
            }
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

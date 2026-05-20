#include "car_modes.h"

static UINT confirm_first_maneuver(t_ultrasonic_data ultrasonic_data)
{
    if (ultrasonic_data.back_distance_cm > FIRST_MANEUVER_SAFE_DISTANCE_CM)
        return 0; // Not close enough to the back wall
    return 1; // Close enough to the back wall
}

static move_backwards(car_t *car, pid_t *throttle_pid, ULONG *last_tick)
{
    float dt = get_delta_time_seconds(last_tick);
    if (dt <= 0.0f)
        dt = 0.01f;

    float throttle_cmd_percent = pidThrottleCalculation(throttle_pid, -0.05f, dt);
    car_set_throttle_percent(car, throttle_cmd_percent, 0); // Move backwards really slowly
}

e_parking_mode park_first_maneuver(car_t *car, pid_t throttle_pid)
{
    t_ultrasonic_data ultrasonic_data;
    bzero(&ultrasonic_data, sizeof(ultrasonic_data));

    ULONG last_tick = tx_time_get();
    while (tx_queue_receive(&g_ultrasonic_data_queue, &ultrasonic_data, TX_WAIT_FOREVER) == TX_SUCCESS)
    {
        if (!is_distance_safe(ultrasonic_data.back_distance_cm, 0))
            return ERROR_MANEUVER;

        move_backwards(car, &throttle_pid, &last_tick);

        if (confirm_first_maneuver(ultrasonic_data))
            return SECOND_MANEUVER;
    }
    return ERROR_MANEUVER;
}

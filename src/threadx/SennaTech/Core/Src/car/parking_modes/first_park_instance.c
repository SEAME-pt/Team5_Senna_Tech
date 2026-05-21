#include "car_modes.h"

static UINT confirm_first_maneuver(t_ultrasonic_data ultrasonic_data)
{
    if (ultrasonic_data.back_distance_cm > FIRST_MANEUVER_SAFE_DISTANCE_CM)
        return 0; // Not close enough to the back wall
    return 1; // Close enough to the back wall
}

e_parking_mode park_first_maneuver(car_t *car)
{
    t_ultrasonic_data ultrasonic_data;
    bzero(&ultrasonic_data, sizeof(ultrasonic_data));

    while (tx_queue_receive(&g_ultrasonic_data_queue, &ultrasonic_data, TX_WAIT_FOREVER) == TX_SUCCESS)
    {
        if (!is_distance_safe(ultrasonic_data.back_distance_cm, 0))
            break ;

        car_set_throttle_percent(car, CONSTANT_PARKING_VELOCITY, 0);

        if (confirm_first_maneuver(ultrasonic_data))
        {
            car_set_throttle_percent(car, 0, 1);
            return SECOND_MANEUVER;
        }
    }
    return ERROR_MANEUVER;
}

#include "car_modes.h"

UINT park_first_maneuver(car_t *car, UINT *parking_mode)
{
    t_ultrasonic_data ultrasonic_data;
    bzero(&ultrasonic_data, sizeof(ultrasonic_data));

    while (tx_queue_receive(&g_ultrasonic_data_queue, &ultrasonic_data, TX_WAIT_FOREVER) == TX_SUCCESS)
    {
        if (!is_distance_safe(ultrasonic_data.back_distance_cm, 0))
            return 1; // end of first maneuver, start second maneuver

        car_set_throttle_percent(car, -0.05f, 0); // Move backwards really slowly
    }
}
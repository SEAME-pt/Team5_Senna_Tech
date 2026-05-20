#include "car_modes.h"

UINT stabilizing_two_values(ULONG value1, ULONG value2)
{
    UINT threshold = 3; // cm

    if (value1 > value2 + threshold) 
        return 0;
    else if (value1 < value2 - threshold) 
        return 0;
    else
        return 1; // close enough, snap to target
}

e_parking_mode park_final_maneuver(car_t *car)
{
    t_ultrasonic_data ultrasonic_data;
    bzero(&ultrasonic_data, sizeof(ultrasonic_data));

    ULONG last_tick = tx_time_get();
    while (tx_queue_receive(&g_ultrasonic_data_queue, &ultrasonic_data, TX_WAIT_FOREVER) == TX_SUCCESS)
    {
        if (!is_distance_safe(ultrasonic_data.back_distance_cm, 0))
            break ;

        car_set_throttle_percent(car, CONSTANT_PARKING_VELOCITY, 0);

        if (confirm_first_maneuver(ultrasonic_data))
        {
            car_set_throttle_percent(car, 0, 1);

            uart_send("Final maneuver complete, car is parked :)\r\n");
            return FINAL_MANEUVER;
        }
    }
    return ERROR_MANEUVER;
}

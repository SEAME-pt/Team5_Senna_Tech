#include "car_modes.h"

UINT stabilizing_two_values(ULONG value1, ULONG value2)
{
    if (value1 > value2 + FINAL_MANEUVER_SAFE_DISTANCE_CM)
        return 0;
    if (value2 > value1 + FINAL_MANEUVER_SAFE_DISTANCE_CM)
        return 0;
    return 1;
}

e_parking_mode park_final_maneuver(car_t *car)
{
    t_ultrasonic_data ultrasonic_data;
    bzero(&ultrasonic_data, sizeof(ultrasonic_data));

    while (tx_queue_receive(&g_ultrasonic_data_queue, &ultrasonic_data, TX_WAIT_FOREVER) == TX_SUCCESS)
    {
        if (!is_distance_safe(ultrasonic_data.back_distance_cm, 0))
            break ;

        car_set_throttle_percent(car, CONSTANT_PARKING_VELOCITY  * -1, 0);

        if (stabilizing_two_values(ultrasonic_data.back_distance_cm, ultrasonic_data.front_distance_cm))
        {
            car_set_throttle_percent(car, 0, 1);

            uart_send("Final maneuver complete, car is parked :)\r\n");
            return FINAL_MANEUVER;
        }
    }

    car_set_throttle_percent(car, 0, 1);
    return ERROR_MANEUVER;
}

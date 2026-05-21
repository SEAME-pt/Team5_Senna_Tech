#include "car_modes.h"

// This function checks if the two values are within a certain distance of each other,
// to detect when the car is in the middle of the parking slot
static UINT stabilizing_two_values(ULONG value1, ULONG value2)
{
    if (value1 > value2 + FINAL_MANEUVER_THRESHOLD_CM)
        return 0;
    if (value2 > value1 + FINAL_MANEUVER_THRESHOLD_CM)
        return 0;
    return 1;
}

static UINT is_front_infinite(ULONG front_distance_cm)
{
    if (front_distance_cm > FINAL_MANEUVER_THRESHOLD_CM * 2)
        return 1;
    return 0;
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

        if (is_front_infinite(ultrasonic_data.front_distance_cm) || 
        stabilizing_two_values(ultrasonic_data.back_distance_cm, ultrasonic_data.front_distance_cm))
        {
            uart_send("Final maneuver complete, car is parked :)\r\n");
            return FINAL_MANEUVER;
        }
    }
    return ERROR_MANEUVER;
}

#include "car_modes.h"

// If the distance is not positive, it means i dont really care to measure it, so its considered safe.
UINT is_distance_safe(ULONG back_distance_cm, ULONG front_distance_cm)
{
    const ULONG safe_distance_threshold_cm = 6; // cm

    if (back_distance_cm && back_distance_cm < safe_distance_threshold_cm) 
        return 0;

    if (front_distance_cm && front_distance_cm < safe_distance_threshold_cm) 
        return 0;

    return 1; // Safe distance
}

void parking_mode_entry(car_t *car, pid_t throttle_pid)
{
    e_parking_mode parking_mode = FIRST_MANEUVER;
    UINT first_time_curving = 1;

    while (1)
    {
        if (first_time_curving)
            car_set_steering_percent(car, 1.0f); // Full right curve

        parking_mode = park_first_maneuver(car, throttle_pid);

        if (parking_mode == ERROR_MANEUVER)
            uart_send("Error during parking maneuver, aborting parking mode\r\n");
        else if (parking_mode == SECOND_MANEUVER)
            uart_send("First maneuver complete, starting second maneuver\r\n");
        
        break ;
    }
}

#include "car_modes.h"

// If some distance is non positive, it means i dont really care to measure it, so its considered safe.
UINT is_distance_safe(ULONG back_distance_cm, ULONG front_distance_cm)
{
    const ULONG safe_distance_threshold_cm = 2; // cm

    if (back_distance_cm && back_distance_cm < safe_distance_threshold_cm) 
        return 0;

    if (front_distance_cm && front_distance_cm < safe_distance_threshold_cm) 
        return 0;

    return 1; // Safe distance
}

void parking_mode_entry(car_t *car)
{
    e_parking_mode parking_mode = FIRST_MANEUVER;
    // ensure car is fully stopped before starting any maneuver
    car_set_throttle_percent(car, 0, 1);

    car_set_steering_percent(car, -1.0f); // Full right
    parking_mode = park_first_maneuver(car);
    if (parking_mode == ERROR_MANEUVER)
    {
        uart_send("Error during first parking maneuver, aborting...\r\n");
        return ;
    }

    car_set_steering_percent(car, 1.0f); // Full left
    parking_mode = park_second_maneuver(car);
    if (parking_mode == ERROR_MANEUVER)
    {
        uart_send("Error during second parking maneuver, aborting...\r\n");
        return ;
    }

    car_set_steering_percent(car, 0.0f); // Centered
    parking_mode = park_final_maneuver(car);
    if (parking_mode == ERROR_MANEUVER)
        uart_send("Error during final parking maneuver, aborting...\r\n");
    car_set_throttle_percent(car, 0, 1);
}

#include "car_modes.h"

// If the distance is 0, it means i dont really care to measure it, so its considered safe.
UINT is_distance_safe(ULONG back_distance_cm, ULONG front_distance_cm)
{
    const ULONG safe_distance_threshold_cm = 6; // cm

    if (back_distance_cm && back_distance_cm < safe_distance_threshold_cm) 
        return 0;

    if (front_distance_cm && front_distance_cm < safe_distance_threshold_cm) 
        return 0;

    return 1; // Safe distance
}

// Parking mode refers to the state of parking the car, 
// which can be either:
// 0 -> First stance of the parking maneuver, where the car is moving backwards towards the parking spot
// 1 -> Second instance of the parking maneuver, where the car is as close to the back wall as possible
// 2 -> Final stance of the parking maneuver, where the car is moving forward to be perfectly parked in the spot
void parking_mode_entry(car_t *car)
{
    UINT parking_mode = 0; // Start with the first stance of the parking maneuver
    UINT first_time_curving = 1;

    while (1)
    {
        if (first_time_curving)
            car_set_steering_percent(&car, 1.0f); // Full right curve

        parking_mode = park_first_maneuver(car, &parking_mode);
    }
}

#ifndef CAR_MODES_H
#define CAR_MODES_H

#include "car.h"

// Distances
#define FIRST_MANEUVER_SAFE_DISTANCE_CM 27
#define SECOND_MANEUVER_SAFE_DISTANCE_CM 14
#define FINAL_MANEUVER_THRESHOLD_CM 20

// Velocities
#define CONSTANT_PARKING_VELOCITY -0.18f

// Parking mode refers to the state of parking the car, 
// which can be either:
// FIRST_MANEUVER  -> First stance of the parking maneuver, 
//                      where the car is moving backwards towards the parking spot
// SECOND_MANEUVER -> Second instance of the parking maneuver, 
//                      where the car is as close to the back wall as possible
// FINAL_MANEUVER  -> Final stance of the parking maneuver, 
//                      where the car is moving forward to be perfectly parked in the spot
typedef enum parking_mode {
    FIRST_MANEUVER  = 0,
    SECOND_MANEUVER = 1,
    FINAL_MANEUVER  = 2,
    ERROR_MANEUVER  = 3
} e_parking_mode;

void parking_mode_entry(car_t *car);
UINT is_distance_safe(ULONG back_distance_cm, ULONG front_distance_cm);

// Parking modes
e_parking_mode park_first_maneuver(car_t *car);
e_parking_mode park_second_maneuver(car_t *car);
e_parking_mode park_final_maneuver(car_t *car);

#endif

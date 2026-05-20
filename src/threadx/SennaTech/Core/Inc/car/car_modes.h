#ifndef CAR_MODES_H
#define CAR_MODES_H

#include "car.h"

typedef enum parking_mode {
    FIRST_MANEUVER  = 0,
    SECOND_MANEUVER = 1,
    FINAL_MANEUVER  = 2,
    ERROR           = 3
} e_parking_mode;

void parking_mode_entry(car_t *car);
UINT is_distance_safe(ULONG back_distance_cm, ULONG front_distance_cm);

// Parking modes
UINT park_first_maneuver(car_t *car, UINT *parking_mode);


#endif
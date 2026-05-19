#ifndef ULTRASONIC_H
#define ULTRASONIC_H

#include "srf08.h"
#include "can_manager.h"

VOID read_front_ultrasonic_distance_cm(ULONG *front_distance_cm);
VOID read_back_ultrasonic_distance_cm(ULONG *back_distance_cm);

#endif

#include "car_modes.h"

void parking_mode_entry(car_t *car)
{
    uart_send("Entering PARKING mode\r\n");
    car_set_throttle_percent(car, 0.0f, 1); // Full brake
    car_set_steering_percent(car, 0.0f);

    
}

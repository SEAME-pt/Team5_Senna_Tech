#include "srf08.h"
#include "can_manager.h"

void ultrasonic_thread_entry(ULONG thread_input)
{
    uart_send("Ultrasonic Thread Entry\r\n");

    int32_t back_distance_cm = 0;
    int32_t front_distance_cm = 0;
    while (1)
    {
        read_back_ultrasonic_distance_cm(&back_distance_cm);
        read_front_ultrasonic_distance_cm(&front_distance_cm);
    }
}
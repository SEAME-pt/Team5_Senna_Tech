#include "ultrasonic.h"

void ultrasonic_thread_entry(ULONG thread_input)
{
    uart_send("Ultrasonic Thread Entry\r\n");

    ULONG back_distance_cm = 0;
    ULONG front_distance_cm = 0;
    while (1)
    {
        // ~1 second between measurements to avoid flooding queues traffic
        tx_thread_sleep(ULTRASONIC_PERIOD_TICKS * 10);

        read_back_ultrasonic_distance_cm(&back_distance_cm);
        read_front_ultrasonic_distance_cm(&front_distance_cm);
    }
}
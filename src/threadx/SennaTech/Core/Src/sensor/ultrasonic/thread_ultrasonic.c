#include "ultrasonic.h"

void ultrasonic_thread_entry(ULONG thread_input)
{
    uart_send("Ultrasonic Thread Entry\r\n");

    t_ultrasonic_data ultrasonic_data;
    bzero(&ultrasonic_data, sizeof(ultrasonic_data));

    while (1)
    {
        read_back_ultrasonic_distance_cm(&ultrasonic_data.back_distance_cm);
        read_front_ultrasonic_distance_cm(&ultrasonic_data.front_distance_cm);

        tx_queue_flush(&g_ultrasonic_data_queue);
        if (tx_queue_send(&g_ultrasonic_data_queue, &ultrasonic_data, TX_NO_WAIT) != TX_SUCCESS)
            uart_send("Failed to send ultrasonic data, probably full :(\r\n");
    }
}

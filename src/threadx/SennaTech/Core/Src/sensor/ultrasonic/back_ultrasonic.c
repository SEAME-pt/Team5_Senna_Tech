#include "srf08.h"

VOID read_back_ultrasonic_distance_cm(int32_t *back_distance_cm)
{
    // ~1 second between measurements to avoid flooding queues traffic
    tx_thread_sleep(ULTRASONIC_PERIOD_TICKS * 10);  
    // Trigger a new ranging cycle
    if (srf08_trigger(&hi2c3, SRF08_DEFAULT_ADDR) != TX_SUCCESS)
    {
        uart_send("[SRF08] Trigger failed\r\n");
        tx_thread_sleep(ULTRASONIC_PERIOD_TICKS);
        *back_distance_cm = -1;
        return ;
    }

    //  Wait for the sensor to finish ranging (~65ms minimum)
    tx_thread_sleep(SRF08_RANGING_DELAY_MS * TX_TIMER_TICKS_PER_SECOND / 1000);

    // Read the result
    if (srf08_read_cm(&hi2c3, SRF08_DEFAULT_ADDR, back_distance_cm) != TX_SUCCESS)
    {
        uart_send("[SRF08] Read failed\r\n");
        tx_thread_sleep(ULTRASONIC_PERIOD_TICKS);
        *back_distance_cm = -1;
        return ;
    }
    uart_send("Distance (cm): ");
    uart_send_int(*back_distance_cm);
    uart_send("\r\n");
}

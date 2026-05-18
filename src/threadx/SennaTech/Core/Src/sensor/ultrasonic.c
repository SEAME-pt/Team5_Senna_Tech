#include "srf08.h"
#include "can_manager.h"

#define ULTRASONIC_PERIOD_MS    100
#define ULTRASONIC_PERIOD_TICKS (ULTRASONIC_PERIOD_MS * TX_TIMER_TICKS_PER_SECOND / 1000)

void ultrasonic_thread_entry(ULONG thread_input)
{
    uart_send("Ultrasonic Thread Entry\r\n");

    while (1)
    {
        tx_thread_sleep(ULTRASONIC_PERIOD_TICKS * 12);

        // 1. Trigger a new ranging cycle
        if (srf08_trigger(SRF08_DEFAULT_ADDR) != TX_SUCCESS)
        {
            uart_send("[SRF08] Trigger failed\r\n");
            tx_thread_sleep(ULTRASONIC_PERIOD_TICKS);
            continue;
        }

        //  2. Wait for the sensor to finish ranging (~65ms minimum)
        tx_thread_sleep(SRF08_RANGING_DELAY_MS * TX_TIMER_TICKS_PER_SECOND / 1000);

        // 3. Read the result
        ULONG distance_cm = 0;
        if (srf08_read_cm(SRF08_DEFAULT_ADDR, &distance_cm) != TX_SUCCESS)
        {
            uart_send("[SRF08] Read failed\r\n");
            tx_thread_sleep(ULTRASONIC_PERIOD_TICKS);
            continue;
        }

        uart_send("Distance (cm): ");
        uart_send_int(distance_cm);
        uart_send("\r\n");
    }
}
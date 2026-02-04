#include "can_manager.h"
#include <stdio.h>

extern volatile uint32_t pulse_count; // Pulse counter (incremented on interrupt)
float speed_kmh = 0.0f;
extern int rpm;
extern uint32_t last_pulse_count;
extern uint32_t last_time_ms;
extern volatile uint32_t last_pulse_time;
extern volatile uint32_t delta_t;
extern volatile float rpm_instant;
extern uint32_t last_print;
extern volatile uint32_t last_interrupt_time;

void sensor_thread_entry(ULONG thread_input)
{
    last_time_ms = tx_time_get();
    last_print = tx_time_get();

	log_debug("SENSOR THREAD STARTED");
	while(1)
	{
        //take the time (Ticks from ThreadX)
        uint32_t current_time = tx_time_get();
		// Check if 100ms have passed (Non-blocking delay)
		if (tx_time_get() - last_print > 100) {
            // Calculate exactly how much time has passed (it could be 101ms, 102ms...)
			uint32_t time_diff = current_time - last_time_ms;

            // Capture current pulses (Snapshot to avoid change during calculation)
			uint32_t current_pulses = pulse_count;
            // Difference in pulses since last reading
			uint32_t pulses_diff = current_pulses - last_pulse_count;

            // RPM calculation
			// FORMULA: (DeltaPulses * 60000 ms) / (DeltaTime * Holes)
			// We use 20 because it is the number of holes in our encoder
			if (time_diff > 0) {
				rpm_instant = (float)(pulses_diff * 60000) / (time_diff * 20);
				rpm = (int)rpm_instant;

                // KM/H = RPM * Circunference * 0.06 (conversion m/min -> km/h)
                // Circunference = Pi * 0.0666
                speed_kmh = rpm_instant * WHEEL_CIRCUMFERENCE * 0.06f;
			} else {
				rpm = 0;
                speed_kmh = 0.0f;
			}

            // Update the "last" variables for the next cycle
			last_pulse_count = current_pulses;
            last_time_ms = current_time;
            last_print = current_time;

		    CAN_Frame speed_frame;
	        speed_frame.id = CAN_ID_SPEED; // ID agreed with Raspberry Pi // Ver Padrao OBD-II
		    speed_frame.dlc = 1;

            // Transmit Speed via CAN
            // Multiply by 100 to send 2 decimal places in an integer
            // Ex: 15.55 km/h becomes 1555. The receiver divides by 100.

		    uint8_t speed_byte = (uint8_t)speed_kmh;

		    // pulse Packaging (Big Endian - Most common in networks)
		    // Byte 0: High range
		    // Byte 1: Low range
		    // cleansing mask & 0xFF
		    speed_frame.data[0] = speed_byte;
			tx_mutex_get(&g_speed_mutex, TX_WAIT_FOREVER);
			vehicle_state.speed_kmh = speed_byte;
			tx_mutex_put(&g_speed_mutex);
            // 4. Send

			if (tx_queue_send(&g_tx_data_queue, &speed_frame, TX_NO_WAIT) != TX_SUCCESS) {
				// Fila cheia: trate erro ou descarte
				log_debug("Error: TX queue full!");
			} /* else {
				log_debug("Frame added: speed=%u", speed_byte);
			} */
		}

/* 		if (MCP2515_ReceiveMessage(&rxFrame) == HAL_OK) {
			log_debug("RX CAN ID=0x%03lX DLC=%d Data=", rxFrame.id, rxFrame.dlc);
				for(int i = 0; i < rxFrame.dlc; i++) {
					log_debug("%02X ", rxFrame.data[i]);
			        log_debug("\n");
				}
		} */
		tx_thread_sleep(1);
	}
}

void sensor_thread_entry2(ULONG thread_input)
{
    last_time_ms = tx_time_get();
    last_pulse_count = pulse_count;

    uint32_t acc_pulses = 0;
    uint32_t acc_ticks  = 0;

    log_debug("SENSOR THREAD2 STARTED");

    while (1)
    {
        uint32_t current_time = tx_time_get();
        uint32_t elapsed_ticks = current_time - last_time_ms;

        /* ========================= */
        /* amostragem a cada 2 ticks (~20ms) */
        /* ========================= */
        if (elapsed_ticks >= 2)
        {
            uint32_t current_pulses = pulse_count;
            uint32_t pulses_diff = current_pulses - last_pulse_count;

            last_pulse_count = current_pulses;
            last_time_ms = current_time;

            acc_pulses += pulses_diff;
            acc_ticks  += elapsed_ticks;
        }

        /* ========================= */
        /* envio a cada 20 ticks (~200ms) */
        /* ========================= */
        if (acc_ticks >= 20)
        {
            if (acc_ticks > 0)
            {
                /* 6000 = 60s * 100 ticks/s */
                rpm_instant =
                    (float)(acc_pulses * 6000) /
                    (acc_ticks * 20);

                rpm = (int)rpm_instant;

                speed_kmh =
                    rpm_instant * WHEEL_CIRCUMFERENCE * 0.06f;
            }
            else
            {
                rpm = 0;
                speed_kmh = 0.0f;
            }

            acc_pulses = 0;
            acc_ticks  = 0;

            /* ===== CAN 1 byte ===== */
            CAN_Frame speed_frame;
            speed_frame.id  = CAN_ID_SPEED;
            speed_frame.dlc = 1;

            uint8_t speed_byte = (uint8_t)speed_kmh;
            speed_frame.data[0] = speed_byte;

            tx_mutex_get(&g_speed_mutex, TX_WAIT_FOREVER);
            vehicle_state.speed_kmh = speed_byte;
            tx_mutex_put(&g_speed_mutex);

            if (tx_queue_send(&g_tx_data_queue, &speed_frame, TX_NO_WAIT) != TX_SUCCESS)
            {
                log_debug("Error: TX queue full!");
            }
        }

        tx_thread_sleep(1); // 1 tick = 10ms
    }
}
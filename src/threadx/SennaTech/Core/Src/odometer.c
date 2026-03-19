#include "can_manager.h"

/*Logica para calculo da distancia percorrida
    18 pulsos = 1 volta = WHEEL_CIRCUMFERENCE(metros)
    portanto:
    1 pulso = WHEEL_CIRCUMFERENCE / 18
    por isso:
    Distancia total percorrida = total de pulsos * (WHEEL_CIRCUMFERENCE / 18)
*/

extern volatile uint32_t pulse_count; // Pulse counter (incremented on interrupt)

void odometer_thread_entry(ULONG thread_input)
{
    uint32_t last_pulse_count = 0;
    uint32_t total_pulses_accum = 0;
    uint32_t delta;
    uint32_t total_distance_mm = 0;
    uint16_t total_distance_m = 0;
    uint16_t last_sent_distance_m = 0;
    while(1)
    {
        delta = pulse_count - last_pulse_count;
        total_pulses_accum += delta;

        total_distance_mm = total_pulses_accum * (WHEEL_CIRCUMFERENCE_MM / 18);
        total_distance_m = total_distance_mm / 1000;
        if (total_distance_m > last_sent_distance_m){
            last_sent_distance_m = total_distance_m;
            //enviar via can
            CAN_Frame odometer_frame;
            odometer_frame.id = CAN_ID_ODOMETER;
            odometer_frame.dlc = 2;
            odometer_frame.data[0] = total_distance_m >> 8 & 0xFF;
            odometer_frame.data[1] = total_distance_m & 0xFF;

            if (tx_queue_send(&g_tx_data_queue, &odometer_frame, TX_NO_WAIT) != TX_SUCCESS) {
				log_debug("Error: TX queue full!");
			}

            tx_mutex_get(&g_odometer_mutex, TX_WAIT_FOREVER);
			vehicle_state.odometer = total_distance_m;
			tx_mutex_put(&g_odometer_mutex);
        }
        last_pulse_count = pulse_count;
        
        tx_thread_sleep(1);
    }
}

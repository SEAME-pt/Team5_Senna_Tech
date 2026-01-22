#include "can_manager.h"
#include <stdio.h>

void battery_thread_entry(ULONG thread_input)
{
	printf("BATTERY THREAD STARTED");
	CAN_Frame batteryFrame;
	batteryFrame.dlc = 1;
	batteryFrame.id = CAN_ID_BATTERY;

	while (1)
	{
		tx_mutex_get(&g_battery_mutex, TX_WAIT_FOREVER);
		vehicle_state.battery_level = 50;
		// LOGICA I2C PARA BUSCAR A VOLTAGEM
		batteryFrame.data[0] = vehicle_state.battery_level;
		tx_mutex_put(&g_battery_mutex);
		if (tx_queue_send(&g_tx_data_queue, &batteryFrame, TX_NO_WAIT) != TX_SUCCESS) {
				// Fila cheia: trate erro ou descarte
			printf("TX queue cheia! Frame descartado.\n");
		} else {
			printf("Frame colocado na queue: battery=%u\n", batteryFrame.data[0]);
		}
		tx_thread_sleep(20);
	}
}
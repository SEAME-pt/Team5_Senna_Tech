#include "can_manager.h"
#include <stdio.h>
#include "ina219.h"

void battery_thread_entry(ULONG thread_input)
{
	printf("BATTERY THREAD STARTED");
	CAN_Frame batteryFrame;
	batteryFrame.dlc = 1;
	batteryFrame.id = CAN_ID_BATTERY;

	INA219_t ina219;

	INA219_Init(&ina219, &hi2c1, INA219_DEFAULT_ADDRESS);
	INA219_SetCalibration32V2A(&ina219);

	while (1)
	{
		tx_mutex_get(&g_battery_mutex, TX_WAIT_FOREVER);

		float voltage = INA219_GetBusVoltage(&ina219);
		int battery_level = (int)(((voltage - BATTERY_VOLTAGE_MIN) / 
								(BATTERY_VOLTAGE_MAX - BATTERY_VOLTAGE_MIN)) * 100);
		if (battery_level < 0) battery_level = 0;
		if (battery_level > 100) battery_level = 100;

		vehicle_state.battery_level = battery_level;
		batteryFrame.data[0] = vehicle_state.battery_level;

		tx_mutex_put(&g_battery_mutex);

		if (tx_queue_send(&g_tx_data_queue, &batteryFrame, TX_NO_WAIT) != TX_SUCCESS) {
			printf("TX queue cheia! Frame descartado.\n");
		} else {
			printf("Frame colocado na queue: battery=%u\n", batteryFrame.data[0]);
		}

		tx_thread_sleep(100);
	}
}
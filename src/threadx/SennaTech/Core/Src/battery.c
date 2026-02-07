#include "can_manager.h"
#include <stdio.h>
#include "ina219.h"
#include <stdbool.h>


void battery_thread_entry(ULONG thread_input)
{
	log_debug("BATTERY THREAD STARTED");
	CAN_Frame batteryFrame;
	batteryFrame.dlc = 1;
	batteryFrame.id = CAN_ID_BATTERY;

	INA219_t ina219;

	INA219_Init(&ina219, &hi2c1, INA219_DEFAULT_ADDRESS);
	INA219_SetCalibration32V2A(&ina219);

	int diff = 0;
	bool first_time = true;

	while (1)
	{
		tx_mutex_get(&g_battery_mutex, TX_WAIT_FOREVER);

		float voltage = INA219_GetBusVoltage(&ina219);
		float current = INA219_GetCurrent(&ina219);

		int battery_level = (int)(((voltage - BATTERY_VOLTAGE_MIN) /
								(BATTERY_VOLTAGE_MAX - BATTERY_VOLTAGE_MIN)) * 100);

		if (battery_level < 0) battery_level = 0;
		if (battery_level > 100) battery_level = 100;

		if (first_time)
		{
			vehicle_state.battery_level = battery_level;
			batteryFrame.data[0] = vehicle_state.battery_level;
			first_time = false;
			diff = 0;
		}
		else if (battery_level != vehicle_state.battery_level)
		{
			diff++;

			if (diff >= 10)
			{
				vehicle_state.battery_level = battery_level;
				batteryFrame.data[0] = vehicle_state.battery_level;
				diff = 0;
			}
		}
		else
		{
			diff = 0;
		}
		tx_mutex_put(&g_battery_mutex);

		if (tx_queue_send(&g_tx_data_queue, &batteryFrame, TX_NO_WAIT) != TX_SUCCESS)
			log_debug("TX queue cheia! Frame descartado.");

		tx_thread_sleep(100);
	}
}
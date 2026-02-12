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

	int current = 0;
	int diff = 0;
	bool first_time = true;

	tx_thread_sleep(600);
	while (1)
	{
		current = INA219_GetCurrent(&ina219);
		tx_mutex_get(&g_battery_mutex, TX_WAIT_FOREVER);

		float voltage = INA219_GetBusVoltage(&ina219);

		int battery_level = (int)(((voltage - BATTERY_VOLTAGE_MIN) /
								(BATTERY_VOLTAGE_MAX - BATTERY_VOLTAGE_MIN)) * 100);

		if (battery_level < 2) battery_level = 1;
		if (battery_level > 100) battery_level = 100;

		bool update = false;

/* 		if (current > 0)
			log_debug("corrente positiva");
		else
			log_debug("corrente negativa"); */

		if (first_time)
		{
			update = true;
			first_time = false;
		}
		else if (current < 0 && battery_level < vehicle_state.battery_level)
		{
			diff += 1;
			if (diff >= 10)
			{
				battery_level = vehicle_state.battery_level - 1;
				update = true;
				diff = 0;
			}
		}
		else if (current > 0 && battery_level > vehicle_state.battery_level)
			update = true;

		if (update)
		{
			vehicle_state.battery_level = battery_level;
			batteryFrame.data[0] = battery_level;
			diff = 0;
		}

		tx_mutex_put(&g_battery_mutex);

		if (tx_queue_send(&g_tx_data_queue, &batteryFrame, TX_NO_WAIT) != TX_SUCCESS)
			log_debug("TX queue cheia! Frame descartado.");

		tx_thread_sleep(150);
	}
}

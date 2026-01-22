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
/* 	printf("Initializing MCP2515...\r\n");

	  // Reset inicial
	  printf("Calling MCP2515_Reset...\n");
	  MCP2515_Reset();
	  tx_thread_sleep(50);
	  printf("Calling MCP2515_Reset...\n");
	//  HAL_Delay(10);
	  // Configure bitrate - THIS FUNCTION ALREADY PUTS YOU IN CONFIG MODE
	  if (MCP2515_SetBitrate(CAN_500KBPS, MCP_8MHZ) != HAL_OK) {
	      printf("ERROR: Bit rate\n");
	  }

	  // Configure filters
	  // Here we have to change things later
	  //there's no standard for arbitration, security, or priority.
	  //We receive everything that comes via the can.
	  //I'll switch after studying the Uprotocol.
	  MCP2515_WriteByte(MCP_RXB0CTRL, 0x60); // Receive all messages
	  MCP2515_WriteByte(MCP_RXM0SIDH, 0x00);
	  MCP2515_WriteByte(MCP_RXM0SIDL, 0x00);
	  MCP2515_WriteByte(MCP_RXM1SIDH, 0x00);
	  MCP2515_WriteByte(MCP_RXM1SIDL, 0x00);

	  // enable interrupts
	  // Receive Buffer 0 Interrupt (RX0IE) to trigger MCU IRQ on new data
	  MCP2515_WriteByte(MCP_CANINTE, 0x01);

	  // Clear all pending interrupt flags to ensure a clean start state
	  MCP2515_WriteByte(MCP_CANINTF, 0x00);

	  // Switch from configuration mode to normal Mode to start bus communication
	  MCP2515_WriteByte(MCP_CANCTRL, MODE_NORMAL);
	//  HAL_Delay(10);

	  // Final verification
	  uint8_t check_inte = MCP2515_ReadByte(MCP_CANINTE);
	  uint8_t check_intf = MCP2515_ReadByte(MCP_CANINTF);
	  uint8_t final_canstat = MCP2515_ReadByte(MCP_CANSTAT);

	  printf("Final check - CANINTE: 0x%02X, CANINTF: 0x%02X, CANSTAT: 0x%02X\n",
	         check_inte, check_intf, final_canstat);

	  if (check_inte == 0x01) {
	      printf("SUCCESS: MCP2515 initialized - interrupts ENABLED\n");
	  } else {
	      printf("ERROR: Interrupts not enabled! CANINTE=0x%02X\n", check_inte);
	  }

	  printf("MCP2515 in NORMAL mode and ready\n"); */

    last_time_ms = tx_time_get();
    last_print = tx_time_get();

	printf("SENSOR THREAD STARTED");
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
		    speed_frame.dlc = 1;    // Sending 1 bytes

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
				printf("TX queue cheia! Frame descartado.\n");
			} else {
				printf("Frame colocado na queue: speed=%u\n", speed_byte);
			}
		}

/* 		if (MCP2515_ReceiveMessage(&rxFrame) == HAL_OK) {
			printf("RX CAN ID=0x%03lX DLC=%d Data=", rxFrame.id, rxFrame.dlc);
				for(int i = 0; i < rxFrame.dlc; i++) {
					printf("%02X ", rxFrame.data[i]);
			        printf("\n");
				}
		} */
		tx_thread_sleep(10);
	}
}
/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    app_threadx.c
  * @author  MCD Application Team
  * @brief   ThreadX applicative file
  ******************************************************************************
    * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "app_threadx.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "mcp2515.h"
#include <string.h>
#include <stdio.h>
#include "core_cm33.h"

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
/* USER CODE BEGIN PV */

// --- Sensor variables---
extern volatile uint32_t pulse_count; // Pulse counter (incremented on interrupt)
extern int rpm;
extern uint32_t last_pulse_count;
extern uint32_t last_time_ms;
extern volatile uint32_t last_pulse_time;
extern volatile uint32_t delta_t;
extern volatile float rpm_instant;
extern uint32_t last_print;
extern volatile uint32_t last_interrupt_time;

// --- CAN variables ---
extern CAN_Frame rxFrame;
extern volatile uint8_t flag_mensagem_recebida; // Flag to process in the loop

TX_THREAD sensor_thread;
UCHAR sensor_thread_stack[1024];

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN PFP */
void sensor_thread_entry(ULONG thread_input);

/* USER CODE END PFP */

/**
  * @brief  Application ThreadX Initialization.
  * @param memory_ptr: memory pointer
  * @retval int
  */
UINT App_ThreadX_Init(VOID *memory_ptr)
{
  UINT ret = TX_SUCCESS;
  /* USER CODE BEGIN App_ThreadX_MEM_POOL */

  tx_thread_create(&sensor_thread,
      						"Sensor Thread",
      		                sensor_thread_entry,
      		                0,
      		                sensor_thread_stack,
      		                sizeof(sensor_thread_stack),
      		                0,
      		                0,
      		                TX_NO_TIME_SLICE,
      		                TX_AUTO_START);

  /* USER CODE END App_ThreadX_MEM_POOL */
  /* USER CODE BEGIN App_ThreadX_Init */
  /* USER CODE END App_ThreadX_Init */

  return ret;
}

  /**
  * @brief  Function that implements the kernel's initialization.
  * @param  None
  * @retval None
  */
void MX_ThreadX_Init(void)
{
  /* USER CODE BEGIN Before_Kernel_Start */

  /* USER CODE END Before_Kernel_Start */

  tx_kernel_enter();

  /* USER CODE BEGIN Kernel_Start_Error */

  /* USER CODE END Kernel_Start_Error */
}

/* USER CODE BEGIN 1 */
void sensor_thread_entry(ULONG thread_input)
{
	printf("Initializing MCP2515...\r\n");

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

	  printf("MCP2515 in NORMAL mode and ready\n");

	while(1)
	{
		// Check if 100ms have passed (Non-blocking delay)
			  if (tx_time_get() - last_print > 100) {
				  last_print = tx_time_get();
				  printf("pulse counting: %lu\n", pulse_count);

		          CAN_Frame frame_envio;
		          frame_envio.id = 0x123; // ID agreed with Raspberry Pi // Ver Padrão OBD-II
		          frame_envio.dlc = 2;    // Sending 2 bytes

		          // 3. pulse Packaging (Big Endian - Most common in networks)
		          // Byte 0: High range
		          // Byte 1: Low range
		          // cleansing mask & 0xFF
		          frame_envio.data[0] = (pulse_count >> 8) & 0xFF;
		          frame_envio.data[1] = (pulse_count) & 0xFF;

		          // 4. Send
		          if (MCP2515_SendMessage(&frame_envio) == HAL_OK) {
		              // dubug
		              printf("TX CAN OK: pulse_count=%lu\n", pulse_count);
		          } else {
		              printf("TX CAN FALHOU\n");
		          }
			  }

				if (MCP2515_ReceiveMessage(&rxFrame) == HAL_OK) {
				  printf("RX CAN ID=0x%03lX DLC=%d Data=", rxFrame.id, rxFrame.dlc);
				  for(int i = 0; i < rxFrame.dlc; i++) {
					  printf("%02X ", rxFrame.data[i]);
			          printf("\n");
				  }
			  }
			  tx_thread_sleep(10);
	}
}

/* USER CODE END 1 */

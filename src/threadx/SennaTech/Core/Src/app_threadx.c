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
#include "can_manager.h"

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

// --- CAN variables ---
extern CAN_Frame rxFrame;
extern volatile uint8_t flag_mensagem_recebida; // Flag to process in the loop

// THREADS

TX_THREAD sensor_thread;
UCHAR sensor_thread_stack[1024];

TX_THREAD battery_thread;
UCHAR battery_thread_stack[1024];

TX_THREAD can_tx_send;
UCHAR tx_send_thread_stack[1024];

TX_THREAD can_rx_receive;
UCHAR rx_rec_thread_stack[1024];

TX_THREAD motor_control;
UCHAR motors_thread_stack[1024];


// QUEUES

TX_QUEUE g_tx_data_queue;
TX_QUEUE g_rx_data_queue;

// MUTEXES

TX_MUTEX g_speed_mutex;
TX_MUTEX g_dc_motor_mutex;
TX_MUTEX g_servo_mutex;
TX_MUTEX g_battery_mutex;

// #define QUEUE_LEN 8

ULONG tx_queue_buffer[QUEUE_LEN * sizeof(CAN_Frame) / sizeof(ULONG)];
ULONG rx_queue_buffer[QUEUE_LEN * sizeof(CAN_Frame) / sizeof(ULONG)];

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN PFP */


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

	tx_mutex_create(&g_speed_mutex, "speed_mutex", TX_NO_INHERIT);
	tx_mutex_create(&g_battery_mutex, "battery_mutex", TX_NO_INHERIT);
	tx_mutex_create(&spi_mutex, "spi_mutex", TX_NO_INHERIT);


  	tx_queue_create(&g_tx_data_queue,
                  "CAN TX Queue",
                  sizeof(CAN_Frame) / sizeof(ULONG),
                  memory_ptr,
                  sizeof(tx_queue_buffer));
	memory_ptr += QUEUE_LEN * sizeof(CAN_Frame);

  	tx_queue_create(&g_rx_data_queue,
                  "CAN RX Queue",
                  sizeof(CAN_Frame) / sizeof(ULONG),
                  memory_ptr,
                  sizeof(rx_queue_buffer));
	memory_ptr += QUEUE_LEN * sizeof(CAN_Frame);

	tx_thread_create(&sensor_thread,
      						"Sensor Thread",
      		                sensor_thread_entry,
      		                0,
      		                sensor_thread_stack,
      		                sizeof(sensor_thread_stack),
      		                10,
      		                10,
      		                TX_NO_TIME_SLICE,
      		                TX_AUTO_START);

	tx_thread_create(&can_tx_send,
      						"Can TX Thread",
      		                CAN_Tx_Thread_Entry,
      		                1,
      		                tx_send_thread_stack,
      		                sizeof(tx_send_thread_stack),
      		                10,
      		                10,
      		                TX_NO_TIME_SLICE,
      		                TX_AUTO_START);

	tx_thread_create(&battery_thread,
      						"Battery Thread",
      		                battery_thread_entry,
      		                1,
      		                battery_thread_stack,
      		                sizeof(battery_thread_stack),
      		                15,
      		                15,
      		                TX_NO_TIME_SLICE,
      		                TX_AUTO_START);
						
	tx_thread_create(&motor_control,
      						"Motors Thread",
      		                motors_thread_entry,
      		                1,
      		                motors_thread_stack,
      		                sizeof(motors_thread_stack),
      		                0,
      		                0,
      		                TX_NO_TIME_SLICE,
      		                TX_AUTO_START);

	tx_thread_create(&can_rx_receive,
      						"CAN RX Thread",
      		                CAN_Rx_Thread_Entry,
      		                1,
      		                rx_rec_thread_stack,
      		                sizeof(rx_rec_thread_stack),
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
  tx_kernel_enter();

  /* USER CODE BEGIN Kernel_Start_Error */

  /* USER CODE END Kernel_Start_Error */
}

/* USER CODE BEGIN 1 */


/* USER CODE END 1 */

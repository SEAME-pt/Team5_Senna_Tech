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
#include "can_manager.h"
#include "utils.h"

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
t_threads   threads[THREAD_COUNT];

// QUEUES
TX_QUEUE g_tx_data_queue;
TX_QUEUE g_rx_data_queue;
TX_QUEUE g_ultrasonic_data_queue;

// MUTEXES
TX_MUTEX g_speed_mutex;
TX_MUTEX g_dc_motor_mutex;
TX_MUTEX g_servo_mutex;
TX_MUTEX g_battery_mutex;
TX_MUTEX g_odometer_mutex;

// #define QUEUE_LEN 8

ULONG tx_queue_buffer[QUEUE_LEN * sizeof(CAN_Frame) / sizeof(ULONG)];
ULONG rx_queue_buffer[QUEUE_LEN * sizeof(CAN_Frame) / sizeof(ULONG)];
ULONG ultrasonic_queue_buffer[QUEUE_LEN * sizeof(t_ultrasonic_data) / sizeof(ULONG)];

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN PFP */

static UINT App_CreateMutexes(void);
static UINT App_CreateQueues(void);
static UINT App_CreateThreads(void);

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
	(void)memory_ptr;

	ret = App_CreateMutexes();
	if (ret != TX_SUCCESS) {
		uart_send("ThreadX mutex init failed!\r\n");
		Error_Handler();
		return ret;
	}

	ret = App_CreateQueues();
	if (ret != TX_SUCCESS) {
		uart_send("ThreadX queue init failed!\r\n");
		Error_Handler();
		return ret;
	}

	ret = App_CreateThreads();
	if (ret != TX_SUCCESS) {
		uart_send("ThreadX thread init failed!\r\n");
		Error_Handler();
		return ret;
	}

	uart_send("ThreadX Initialized\r\n");

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
  
  /* if (MCP2515_Init() != HAL_OK) {
	  uart_send("MCP2515 init failed!\r\n");
	  Error_Handler();
  } */
  
  /* USER CODE END Before_Kernel_Start */

  tx_kernel_enter();

  /* USER CODE BEGIN Kernel_Start_Error */

  /* USER CODE END Kernel_Start_Error */
}

/* USER CODE BEGIN 1 */

static UINT App_CreateMutexes(void)
{
	UINT ret;

	ret = tx_mutex_create(&g_speed_mutex, "speed_mutex", TX_NO_INHERIT);
	if (ret != TX_SUCCESS) {
		return ret;
	}

	ret = tx_mutex_create(&g_battery_mutex, "battery_mutex", TX_NO_INHERIT);
	if (ret != TX_SUCCESS) {
		return ret;
	}

	ret = tx_mutex_create(&spi_mutex, "spi_mutex", TX_NO_INHERIT);
	if (ret != TX_SUCCESS) {
		return ret;
	}

	return TX_SUCCESS;
}

static UINT App_CreateQueues(void)
{
	UINT ret;

	ret = tx_queue_create(&g_tx_data_queue,
					  "CAN TX Queue",
					  sizeof(CAN_Frame) / sizeof(ULONG),
					  tx_queue_buffer,
					  sizeof(tx_queue_buffer));
	if (ret != TX_SUCCESS) {
		uart_send("Failed to create CAN TX queue!\r\n");
		return ret;
	}

	ret = tx_queue_create(&g_rx_data_queue,
					  "CAN RX Queue",
					  sizeof(CAN_Frame) / sizeof(ULONG),
					  rx_queue_buffer,
					  sizeof(rx_queue_buffer));
	if (ret != TX_SUCCESS) {
		uart_send("Failed to create CAN RX queue!\r\n");
		return ret;
	}

	ret = tx_queue_create(&g_ultrasonic_data_queue,
					  "Ultrasonic Queue",
					  sizeof(t_ultrasonic_data) / sizeof(ULONG),
					  ultrasonic_queue_buffer,
					  sizeof(ultrasonic_queue_buffer));
	if (ret != TX_SUCCESS) {
		uart_send("Failed to create Ultrasonic queue!\r\n");
		return ret;
	}
	
	return TX_SUCCESS;
}

static UINT App_CreateThreads(void)
{
	UINT ret;

	/* ret = tx_thread_create(&threads[0].thread,
				       "Sensor Thread",
				       sensor_thread_entry2,
				       0,
				       threads[0].stack,
				       sizeof(threads[0].stack),
				       14, 14, 
					   TX_NO_TIME_SLICE, TX_AUTO_START);
	if (ret != TX_SUCCESS) {
		uart_send("Failed to create Sensor thread!\r\n");
		return ret;
	}

	ret = tx_thread_create(&threads[1].thread,
				       "Can TX Thread",
				       CAN_Tx_Thread_Entry,
				       1,
				       threads[1].stack,
				       sizeof(threads[1].stack),
				       10, 10,
					   TX_NO_TIME_SLICE, TX_AUTO_START);
	if (ret != TX_SUCCESS) {
		uart_send("Failed to create CAN TX thread!\r\n");
		return ret;
	}

	ret = tx_thread_create(&threads[2].thread,
				       "Battery Thread",
				       battery_thread_entry,
				       1,
				       threads[2].stack,
				       sizeof(threads[2].stack),
				       15, 15,
					   TX_NO_TIME_SLICE, TX_AUTO_START);
	if (ret != TX_SUCCESS) {
		uart_send("Failed to create Battery thread!\r\n");
		return ret;
	}

	ret = tx_thread_create(&threads[3].thread,
				       "Motors Thread",
				       motors_thread_entry,
				       1,
				       threads[3].stack,
				       sizeof(threads[3].stack),
				       1, 1,
					   TX_NO_TIME_SLICE, TX_AUTO_START);
	if (ret != TX_SUCCESS) {
		uart_send("Failed to create Motors thread!\r\n");
		return ret;
	}

	ret = tx_thread_create(&threads[4].thread,
				       "CAN RX Thread",
				       CAN_Rx_Thread_Entry,
				       1,
				       threads[4].stack,
				       sizeof(threads[4].stack),
				       1, 1,
					   TX_NO_TIME_SLICE, TX_AUTO_START);
	if (ret != TX_SUCCESS) {
		uart_send("Failed to create CAN RX thread!\r\n");
		return ret;
	}

	ret = tx_thread_create(&threads[5].thread,
				       "Heartbeat Thread",
				       heartbeat_thread_entry,
				       0,
				       threads[5].mini_stack,
				       sizeof(threads[5].mini_stack),
				       16, 16,
					   TX_NO_TIME_SLICE, TX_AUTO_START);
	if (ret != TX_SUCCESS) {
		uart_send("Failed to create Heartbeat thread!\r\n");
		return ret;
	}

	ret = tx_thread_create(&threads[6].thread,
				       "ultrasonic Thread",
				       ultrasonic_thread_entry,
				       0,
				       threads[6].stack,
				       sizeof(threads[6].stack),
				       12, 12,
					   TX_NO_TIME_SLICE, TX_AUTO_START);
	if (ret != TX_SUCCESS) {
		uart_send("Failed to create ultrasonic thread!\r\n");
		return ret;
	} */

	ret = tx_thread_create(&threads[7].thread,
				       "OLED Thread",
				       oled_thread_entry,
				       0,
				       threads[7].stack,
				       sizeof(threads[7].stack),
				       12, 12,
					   TX_NO_TIME_SLICE, TX_AUTO_START);
	if (ret != TX_SUCCESS) {
		uart_send("Failed to create OLED thread!\r\n");
		return ret;
	}

	return TX_SUCCESS;
}

/* USER CODE END 1 */

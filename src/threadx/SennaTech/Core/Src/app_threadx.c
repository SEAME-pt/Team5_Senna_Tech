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

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

typedef enum {
    THREAD_SENSOR = 0,
    THREAD_CAN_TX,
    THREAD_CAN_RX,
    THREAD_BATTERY,
    THREAD_MOTOR,
    THREAD_DEBUG,
    THREAD_HEARTBEAT,
    THREAD_COUNT
} thread_idx_t;

typedef struct {
    TX_THREAD   handle;
    UCHAR       stack[1024];
} t_thread;

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
static t_thread threads[THREAD_COUNT];

// QUEUES
TX_QUEUE g_tx_data_queue;
TX_QUEUE g_rx_data_queue;

// MUTEXES
TX_MUTEX g_speed_mutex;
TX_MUTEX g_dc_motor_mutex;
TX_MUTEX g_servo_mutex;
TX_MUTEX g_battery_mutex;
TX_MUTEX g_odometer_mutex;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN PFP */

static UINT init_mutexes(void);
static UINT init_queues(VOID *memory_ptr);
static UINT init_threads(void);

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

    ret = init_mutexes();
    if (ret != TX_SUCCESS) 
		return ret;

    ret = init_queues(memory_ptr);
    if (ret != TX_SUCCESS) 
		return ret;

    ret = init_threads();
    if (ret != TX_SUCCESS) 
		return ret;

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
  
  if (MCP2515_Init() != HAL_OK) {
	  uart_send("MCP2515 init failed!");
	  Error_Handler();
  }

  /* USER CODE END Before_Kernel_Start */

  tx_kernel_enter();

  /* USER CODE BEGIN Kernel_Start_Error */

  /* USER CODE END Kernel_Start_Error */
}

/* USER CODE BEGIN 1 */

static UINT init_mutexes(void)
{
    UINT ret;

    ret = tx_mutex_create(&g_speed_mutex, "speed_mutex", TX_NO_INHERIT);
    if (ret != TX_SUCCESS) { uart_send("ERROR: speed_mutex creation failed\r\n"); return ret; }

    ret = tx_mutex_create(&g_battery_mutex, "battery_mutex", TX_NO_INHERIT);
    if (ret != TX_SUCCESS) { uart_send("ERROR: battery_mutex creation failed\r\n"); return ret; }

    ret = tx_mutex_create(&spi_mutex, "spi_mutex", TX_NO_INHERIT);
    if (ret != TX_SUCCESS) { uart_send("ERROR: spi_mutex creation failed\r\n"); return ret; }

    return TX_SUCCESS;
}

static UINT init_queues(VOID *memory_ptr)
{
    UINT  ret;
    UCHAR *ptr = (UCHAR *)memory_ptr;

    ret = tx_queue_create(&g_tx_data_queue, "CAN TX Queue",
                          sizeof(CAN_Frame) / sizeof(ULONG),
                          ptr, QUEUE_LEN * sizeof(CAN_Frame));
    if (ret != TX_SUCCESS) { uart_send("ERROR: CAN TX queue creation failed\r\n"); return ret; }
    ptr += QUEUE_LEN * sizeof(CAN_Frame);

    ret = tx_queue_create(&g_rx_data_queue, "CAN RX Queue",
                          sizeof(CAN_Frame) / sizeof(ULONG),
                          ptr, QUEUE_LEN * sizeof(CAN_Frame));
    if (ret != TX_SUCCESS) { uart_send("ERROR: CAN RX queue creation failed\r\n"); return ret; }
    ptr += QUEUE_LEN * sizeof(CAN_Frame);

    return TX_SUCCESS;
}

static UINT init_threads(void)
{
    UINT ret;

    ret = tx_thread_create(&threads[THREAD_SENSOR].handle, "Sensor Thread",
                           sensor_thread_entry2, 0,
                           threads[THREAD_SENSOR].stack, sizeof(threads[THREAD_SENSOR].stack),
                           10, 10, TX_NO_TIME_SLICE, TX_AUTO_START);
    if (ret != TX_SUCCESS) { uart_send("ERROR: Sensor thread creation failed\r\n"); return ret; }

    ret = tx_thread_create(&threads[THREAD_CAN_TX].handle, "CAN TX Thread",
                           CAN_Tx_Thread_Entry, 1,
                           threads[THREAD_CAN_TX].stack, sizeof(threads[THREAD_CAN_TX].stack),
                           10, 10, TX_NO_TIME_SLICE, TX_AUTO_START);
    if (ret != TX_SUCCESS) { uart_send("ERROR: CAN TX thread creation failed\r\n"); return ret; }

    ret = tx_thread_create(&threads[THREAD_CAN_RX].handle, "CAN RX Thread",
                           CAN_Rx_Thread_Entry, 1,
                           threads[THREAD_CAN_RX].stack, sizeof(threads[THREAD_CAN_RX].stack),
                           1, 1, TX_NO_TIME_SLICE, TX_AUTO_START);
    if (ret != TX_SUCCESS) { uart_send("ERROR: CAN RX thread creation failed\r\n"); return ret; }

    ret = tx_thread_create(&threads[THREAD_BATTERY].handle, "Battery Thread",
                           battery_thread_entry, 1,
                           threads[THREAD_BATTERY].stack, sizeof(threads[THREAD_BATTERY].stack),
                           15, 15, TX_NO_TIME_SLICE, TX_AUTO_START);
    if (ret != TX_SUCCESS) { uart_send("ERROR: Battery thread creation failed\r\n"); return ret; }

    ret = tx_thread_create(&threads[THREAD_MOTOR].handle, "Motors Thread",
                           motors_thread_entry, 1,
                           threads[THREAD_MOTOR].stack, sizeof(threads[THREAD_MOTOR].stack),
                           1, 1, TX_NO_TIME_SLICE, TX_AUTO_START);
    if (ret != TX_SUCCESS) { uart_send("ERROR: Motor thread creation failed\r\n"); return ret; }

    ret = tx_thread_create(&threads[THREAD_DEBUG].handle, "Debug Thread",
                           debug_thread_entry, 1,
                           threads[THREAD_DEBUG].stack, sizeof(threads[THREAD_DEBUG].stack),
                           20, 20, TX_NO_TIME_SLICE, TX_AUTO_START);
    if (ret != TX_SUCCESS) { uart_send("ERROR: Debug thread creation failed\r\n"); return ret; }

    ret = tx_thread_create(&threads[THREAD_HEARTBEAT].handle, "Heartbeat Thread",
                           heartbeat_thread_entry, 0,
                           threads[THREAD_HEARTBEAT].stack, sizeof(threads[THREAD_HEARTBEAT].stack),
                           16, 16, TX_NO_TIME_SLICE, TX_AUTO_START);
    if (ret != TX_SUCCESS) { uart_send("ERROR: Heartbeat thread creation failed\r\n"); return ret; }

    return TX_SUCCESS;
}

/* USER CODE END 1 */

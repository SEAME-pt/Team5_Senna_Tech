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
#include "can_manager.h"
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

TX_THREAD tx_thread;
TX_THREAD rx_thread;
TX_MUTEX spi_mutex;
TX_SEMAPHORE rx_sem;

UCHAR tx_stack[1024];
UCHAR rx_stack[1024];
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

    // criar Mutex (Proteção do SPI)
    tx_mutex_create(&spi_mutex, "SPI Mutex", TX_NO_INHERIT);

    // Criar Semáforo (Sinalização de RX)
    // Contador inicial 0 (ninguém enviou nada ainda)
    tx_semaphore_create(&rx_sem, "RX Semaphore", 0);

    // Criar Thread de Envio
    tx_thread_create(&tx_thread, "CAN TX Thread", 
                     CAN_Tx_Thread_Entry, 0,
                     tx_stack, sizeof(tx_stack),
                     10, 10, TX_NO_TIME_SLICE, TX_AUTO_START); // prioridade 0 mais baixa

    // 4. Criar Thread de Recepção
    // Nota: Dê prioridade MAIOR (número menor) para RX para não perder dados
    tx_thread_create(&rx_thread, "CAN RX Thread", 
                     CAN_Rx_Thread_Entry, 0,
                     rx_stack, sizeof(rx_stack),
                     0, 0, TX_NO_TIME_SLICE, TX_AUTO_START); // Prioridade 0 mais alta

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

  /* USER CODE END Before_Kernel_Start */

  tx_kernel_enter();

  /* USER CODE BEGIN Kernel_Start_Error */

  /* USER CODE END Kernel_Start_Error */
}


/* USER CODE BEGIN 1 */
// Callback do HAL (Interrupção física do pino)
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
  // Interrupção do Sensor de Velocidade (EXTI0)
  if (GPIO_Pin == D0_LM393_Pin) {
      pulse_count++;
  }
  
  // Interrupção do CAN (EXTI7 - MCP2515)
  if (GPIO_Pin == MCP_INT_Pin) {
      // Avisa a thread do CAN Manager que chegou dado
      tx_semaphore_ceiling_put(&rx_sem, 1); 
  }
}
/* USER CODE END 1 */

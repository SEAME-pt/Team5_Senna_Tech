/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    app_threadx.h
  * @author  MCD Application Team
  * @brief   ThreadX applicative header file
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

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __APP_THREADX_H
#define __APP_THREADX_H
#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "tx_api.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

#include <main.h>
#include <string.h>
#include <stdio.h>
#include "i2c.h"
#include <stdarg.h>
#include <inttypes.h>
#include "i2c_hal.h"
#include "sleep_hal.h"
#include "can_manager.h"
#include "mcp2515.h"

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Private defines -----------------------------------------------------------*/

/* USER CODE BEGIN PD */

#define QUEUE_LEN 10
#define LOG_QUEUE_LEN 16
#define LOG_MSG_LEN 64
#define WHEEL_DIAMETER_M  0.0666f
#define WHEEL_DIAMETER_MM  66.666f
#define WHEEL_CIRCUMFERENCE (3.14159f * WHEEL_DIAMETER_M)
#define WHEEL_CIRCUMFERENCE_MM (3.14159f * WHEEL_DIAMETER_MM)
#define ENCODER_HOLES     20

typedef struct {
    char msg[LOG_MSG_LEN];
} log_msg_t;

/* USER CODE END PD */

/* Main thread defines -------------------------------------------------------*/
/* USER CODE BEGIN MTD */

/* USER CODE END MTD */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
UINT App_ThreadX_Init(VOID *memory_ptr);
void MX_ThreadX_Init(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* USER CODE BEGIN 1 */


// QUEUES
extern TX_QUEUE g_tx_data_queue;
extern TX_QUEUE g_rx_data_queue;
extern TX_QUEUE g_log_queue;

//MUTEXES
extern TX_MUTEX g_speed_mutex;
extern TX_MUTEX g_dc_motor_mutex;
extern TX_MUTEX g_servo_mutex;
extern TX_MUTEX g_battery_mutex;

// THREAD ENTRYS
void sensor_thread_entry2(ULONG thread_input);
void sensor_thread_entry(ULONG thread_input);
void battery_thread_entry(ULONG thread_input);
void motors_thread_entry(ULONG thread_input);
void debug_thread_entry(ULONG thread_input);
void heartbeat_thread_entry(ULONG thread_input);

// UTILS
void log_debug(const char *fmt, ...);


/* USER CODE END 1 */

#ifdef __cplusplus
}
#endif
#endif /* __APP_THREADX_H */

#ifndef UTILS_H_
 #define UTILS_H_

#include "app_threadx.h"
#include <stdio.h>

extern UART_HandleTypeDef   huart1;

HAL_StatusTypeDef   i2c_scan_bus(VOID);
VOID                uart_send(const char *msg);
VOID                uart_send_int(int32_t value);
VOID                battery_debug_print(float voltage);
VOID                rpm_debug_print(ULONG rpm, 
                        ULONG cr1_reg, ULONG cnt_reg);

#endif
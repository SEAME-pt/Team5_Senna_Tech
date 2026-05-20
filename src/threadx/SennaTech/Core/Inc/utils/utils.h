#ifndef UTILS_H_
 #define UTILS_H_

#include "app_threadx.h"
#include <stdio.h>

extern UART_HandleTypeDef   huart1;

// Debug
VOID    uart_send(const char *msg);
VOID    uart_send_int(ULONG value);

// Utils
UINT stabilizing_two_values(ULONG value1, ULONG value2);

#endif
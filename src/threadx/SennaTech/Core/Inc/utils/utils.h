#ifndef UTILS_H_
 #define UTILS_H_

#include "app_threadx.h"
#include <stdio.h>

extern UART_HandleTypeDef   huart1;

VOID    uart_send(const char *msg);
VOID    uart_send_int(int32_t value);

#endif
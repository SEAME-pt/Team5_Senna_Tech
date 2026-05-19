#include "utils.h"

// Function to send a string over UART
VOID    uart_send(const char *msg) 
{
    HAL_UART_Transmit(&huart1, (uint8_t*)msg, strlen(msg), 100);
}

// Function to send an integer over UART
VOID    uart_send_int(ULONG value) 
{
    char buffer[12]; // capacity of -2147483648 + null terminator
    snprintf(buffer, sizeof(buffer), "%ld", value);
    uart_send(buffer);
}

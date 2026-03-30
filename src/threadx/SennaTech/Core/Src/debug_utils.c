#include "utils.h"

// Function to send a string over UART
VOID    uart_send(const char *msg) 
{
    HAL_UART_Transmit(&huart1, (uint8_t*)msg, strlen(msg), 100);
}

// Function to send an integer over UART
VOID    uart_send_int(int32_t value) 
{
    char buffer[12]; // capacity of -2147483648 + null terminator
    snprintf(buffer, sizeof(buffer), "%ld", value);
    uart_send(buffer);
}

// Function to print RPM debug information over UART
VOID    rpm_debug_print(ULONG rpm, ULONG cr1_reg, ULONG cnt_reg) {

    char debug[32];

    int len = snprintf(debug, sizeof(debug),
            "RPM=%lu | CR1=%lu | CNT=%lu\r\n",
            rpm, cr1_reg, cnt_reg);

    if (len > 0 && (size_t)len < sizeof(debug))
        HAL_UART_Transmit(&huart1, (uint8_t *)debug, len, 100);
}

VOID    battery_debug_print(float voltage)
{
    uart_send("Battery Voltage: ");
    uart_send_int((int32_t)(voltage * 1000)); // in mV
    uart_send(" mV\r\n");

    uart_send("Battery Percentage: ");
    uart_send_int((int32_t)((voltage / 12.444f) * 100)); // in percentage
    uart_send(" %\r\n");
}
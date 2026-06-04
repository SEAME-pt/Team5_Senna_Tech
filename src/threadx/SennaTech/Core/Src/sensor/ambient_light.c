#include "ambient_light.h"
#include "app_threadx.h"
#include "i2c.h"
#include <string.h>
#include <stdio.h>

UINT AmbientLight_Init(I2C_HandleTypeDef *hi2c, uint16_t addr)
{
    uint8_t payload[2] = {
        AMBIENT_LIGHT_COMMAND_BIT | AMBIENT_LIGHT_REG_CONTROL,
        AMBIENT_LIGHT_CMD_POWERON
    };

    if (HAL_I2C_Master_Transmit(hi2c, addr, payload, sizeof(payload), HAL_MAX_DELAY) != HAL_OK)
    {
        return TX_TIMER_ERROR;
    }

    return TX_SUCCESS;
}

UINT AmbientLight_ReadRaw(I2C_HandleTypeDef *hi2c, uint16_t addr, uint16_t *raw_value)
{
    uint8_t reg = AMBIENT_LIGHT_COMMAND_BIT | AMBIENT_LIGHT_REG_DATA0LOW;
    uint8_t data[2] = {0};

    if (HAL_I2C_Master_Transmit(hi2c, addr, &reg, 1, HAL_MAX_DELAY) != HAL_OK)
    {
        return TX_TIMER_ERROR;
    }

    if (HAL_I2C_Master_Receive(hi2c, addr, data, sizeof(data), HAL_MAX_DELAY) != HAL_OK)
    {
        return TX_TIMER_ERROR;
    }

    *raw_value = (uint16_t)((data[1] << 8) | data[0]);
    return TX_SUCCESS;
}

UINT AmbientLight_ReadLux(I2C_HandleTypeDef *hi2c, uint16_t addr, float *lux)
{
    uint16_t raw_value = 0;

    if (AmbientLight_ReadRaw(hi2c, addr, &raw_value) != TX_SUCCESS)
    {
        return TX_TIMER_ERROR;
    }

    /* Raw value is returned as-is. Update conversion according to your sensor datasheet. */
    *lux = (float)raw_value;
    return TX_SUCCESS;
}

void ambient_thread_entry(ULONG thread_input)
{
    (void)thread_input;

    uart_send("Ambient Thread Entry\r\n");

    t_ambient_data ambient_data;
    memset(&ambient_data, 0, sizeof(ambient_data));

    if (AmbientLight_Init(&hi2c1, AMBIENT_LIGHT_DEFAULT_ADDR) != TX_SUCCESS)
    {
        uart_send("Ambient sensor init failed!\r\n");
    }

    while (1)
    {
        uint16_t raw_light = 0;

        if (AmbientLight_ReadRaw(&hi2c1, AMBIENT_LIGHT_DEFAULT_ADDR, &raw_light) == TX_SUCCESS)
        {
            ambient_data.ambient_light_lux = (float)raw_light;
        }
        else
        {
            ambient_data.ambient_light_lux = -1.0f;
            uart_send("Ambient light read failed!\r\n");
        }

        tx_queue_flush(&g_ambient_data_queue);
        if (tx_queue_send(&g_ambient_data_queue, &ambient_data, TX_NO_WAIT) != TX_SUCCESS)
        {
            uart_send("Ambient queue full!\r\n");
        }

        char buffer[64];
        int length = snprintf(buffer, sizeof(buffer), "Ambient raw light: %u\r\n", raw_light);
        if (length > 0)
        {
            uart_send(buffer);
        }

        tx_thread_sleep(10);
    }
}

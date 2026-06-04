#include "ambient_light.h"

UINT AmbientLight_Init(I2C_HandleTypeDef *hi2c, uint16_t addr)
{
    uint8_t config[2];

    config[0] = AMBIENT_LIGHT_CONF_DEFAULT_LSB;
    config[1] = AMBIENT_LIGHT_CONF_DEFAULT_MSB;

    tx_mutex_get(&g_i2c2_mutex, TX_WAIT_FOREVER);
    if (HAL_I2C_Mem_Write(hi2c,
            addr,
            AMBIENT_LIGHT_REG_ALS_CONF,
            I2C_MEMADD_SIZE_8BIT,
            config,
            2,
            HAL_MAX_DELAY) != HAL_OK)
    {
        tx_mutex_put(&g_i2c2_mutex);
        return (TX_NOT_AVAILABLE);
    }
    tx_mutex_put(&g_i2c2_mutex);

    tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND / 5);

    return (TX_SUCCESS);
}

UINT AmbientLight_ReadRaw(I2C_HandleTypeDef *hi2c,
        uint16_t addr, uint16_t *raw_value)
{
    uint8_t data[2];

    if (raw_value == NULL)
        return (TX_NOT_AVAILABLE);

    data[0] = 0;
    data[1] = 0;

    tx_mutex_get(&g_i2c2_mutex, TX_WAIT_FOREVER);
    if (HAL_I2C_Mem_Read(hi2c,
            addr,
            AMBIENT_LIGHT_REG_ALS,
            I2C_MEMADD_SIZE_8BIT,
            data,
            2,
            HAL_MAX_DELAY) != HAL_OK)
    {
        tx_mutex_put(&g_i2c2_mutex);
        return (TX_NOT_AVAILABLE);
    }
    tx_mutex_put(&g_i2c2_mutex);

    *raw_value = ((uint16_t)data[1] << 8) | data[0];

    return (TX_SUCCESS);
}

UINT AmbientLight_ReadLux(I2C_HandleTypeDef *hi2c,
        uint16_t addr, float *lux)
{
    uint16_t raw_value;

    if (lux == NULL)
        return (TX_NOT_AVAILABLE);

    raw_value = 0;

    if (AmbientLight_ReadRaw(hi2c, addr, &raw_value) != TX_SUCCESS)
        return (TX_NOT_AVAILABLE);

    *lux = (float)raw_value;

    return (TX_SUCCESS);
}

void ambient_thread_entry(ULONG thread_input)
{
    t_ambient_data  ambient_data;
    uint16_t        raw_light;

    uart_send("Ambient Thread Entry\r\n");

    memset(&ambient_data, 0, sizeof(ambient_data));

    if (AmbientLight_Init(&hi2c2, AMBIENT_LIGHT_DEFAULT_ADDR) != TX_SUCCESS)
        uart_send("Ambient sensor init failed!\r\n");

    while (1)
    {
        raw_light = 0;

        if (AmbientLight_ReadRaw(&hi2c2, AMBIENT_LIGHT_DEFAULT_ADDR, &raw_light) == TX_SUCCESS)
            ambient_data.ambient_light_lux = (float)raw_light;
        else
        {
            ambient_data.ambient_light_lux = -1.0f;
            uart_send("Ambient light read failed!\r\n");
        }

        tx_queue_flush(&g_ambient_data_queue);
        if (tx_queue_send(&g_ambient_data_queue, &ambient_data, TX_NO_WAIT) != TX_SUCCESS)
            uart_send("Ambient queue full!\r\n");

        uart_send("Ambient raw light: ");
        uart_send_int(raw_light);
        uart_send("\r\n");

        tx_thread_sleep(300);
    }
}

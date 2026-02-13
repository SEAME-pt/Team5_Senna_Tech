#include "i2c_hal.h"
#include "app_threadx.h"

int I2C_WriteReg(void *hi2c, uint8_t addr, uint8_t reg, uint8_t data)
{
    return HAL_I2C_Mem_Write(
        hi2c, addr, reg,
        I2C_MEMADD_SIZE_8BIT,
        &data, 1, HAL_MAX_DELAY
    );
}

int I2C_ReadReg(void *hi2c, uint8_t addr, uint8_t reg, uint8_t *data)
{
    return HAL_I2C_Mem_Read(
        hi2c, addr, reg,
        I2C_MEMADD_SIZE_8BIT,
        data, 1, HAL_MAX_DELAY
    );
}
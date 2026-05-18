#include "srf08.h"

UINT    srf08_trigger(uint16_t addr)
{
    uint8_t   buff[2] = { SRF08_REG_CMD, SRF08_CMD_RANGE_CM };
    
     // Write 0x51 to register 0x00 to start a ranging cycle in cm
    if (HAL_I2C_Master_Transmit(&hi2c3, addr, buff, 2, 100) != HAL_OK)
        return TX_TIMER_ERROR;
    return TX_SUCCESS;
}

ULONG    srf08_read_cm(uint16_t addr, ULONG *distance_cm)
{
    uint8_t reg  = SRF08_REG_RANGE_HIGH;
    uint8_t data[2];
    
    // Read the high byte of the range
    if (HAL_I2C_Master_Transmit(&hi2c3, addr, &reg, 1, 100) != HAL_OK)
        return TX_TIMER_ERROR;

    // Read 2 bytes (high, low)
    if (HAL_I2C_Master_Receive(&hi2c3, addr, data, 2, 100) != HAL_OK)
        return TX_TIMER_ERROR;
    
    *distance_cm = (ULONG)((data[0] << 8) | data[1]);
    return TX_SUCCESS;
}

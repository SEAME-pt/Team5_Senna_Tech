#include "srf08.h"

UINT    srf08_init(UINT addr)
{
    UINT   ret;
    UINT   buff[2] = { SRF08_REG_CMD, SRF08_CMD_RANGE_CM };
    
     // Write 0x51 to register 0x00 to start a ranging cycle in cm
    if (HAL_I2C_Master_Transmit(&hi2c3, addr, buff, 2, 100) != HAL_OK)
        return TX_TIMER_ERROR;
    return TX_SUCCESS;
}

#ifndef I2C_HAL_H
#define I2C_HAL_H

#include <stdint.h>

int I2C_WriteReg(void *hi2c, uint8_t addr, uint8_t reg, uint8_t data);
int I2C_ReadReg(void *hi2c, uint8_t addr, uint8_t reg, uint8_t *data);

#endif

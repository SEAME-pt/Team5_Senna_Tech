#ifndef AMBIENT_LIGHT_H
#define AMBIENT_LIGHT_H

#include "utils.h"
#include "i2c.h"

/*
 * Onboard ambient light sensor
 * VEML3235 7-bit I2C address: 0x10
 * STM32 HAL uses 8-bit address format: 0x10 << 1 = 0x20
 */

#define AMBIENT_LIGHT_DEFAULT_ADDR      (0x10U << 1)

/*
 * VEML3235 register map
 */
#define AMBIENT_LIGHT_REG_ALS_CONF      0x00U
#define AMBIENT_LIGHT_REG_WHITE         0x04U
#define AMBIENT_LIGHT_REG_ALS           0x05U


#define AMBIENT_LIGHT_CONF_DEFAULT_LSB  0x00U
#define AMBIENT_LIGHT_CONF_DEFAULT_MSB  0x00U

UINT AmbientLight_Init(I2C_HandleTypeDef *hi2c, uint16_t addr);
UINT AmbientLight_ReadRaw(I2C_HandleTypeDef *hi2c,
        uint16_t addr, uint16_t *raw_value);
UINT AmbientLight_ReadLux(I2C_HandleTypeDef *hi2c,
        uint16_t addr, float *lux);

#endif
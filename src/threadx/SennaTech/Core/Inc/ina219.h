#ifndef INA219_H
#define INA219_H
#pragma once
#include <stdint.h>
#include "app_threadx.h"

#define INA219_DEFAULT_ADDRESS 0x41 << 1
#define BATTERY_VOLTAGE_MIN 9.3f
#define BATTERY_VOLTAGE_MAX 12.6f

#define REG_CONFIG        0x00
#define REG_SHUNTVOLTAGE  0x01
#define REG_BUSVOLTAGE    0x02
#define REG_POWER         0x03
#define REG_CURRENT       0x04
#define REG_CALIBRATION   0x05

// Config defaults
#define BUS_VOLTAGE_RANGE_32V 0x01
#define GAIN_DIV_8_320MV      0x03
#define ADC_RES_12BIT_1S      0x03
#define MODE_SANDBVOLT_CONTINUOUS 0x07

typedef struct {
    I2C_HandleTypeDef *hi2c;
    uint8_t addr;
    float currentLSB; // 100uA per bit
    float powerLSB;   // 2mW per bit
} INA219_t;

/* Funções públicas */
void INA219_Init(INA219_t *ina, I2C_HandleTypeDef *hi2c, uint8_t addr);
void INA219_SetCalibration32V2A(INA219_t *ina);

float INA219_GetBusVoltage(INA219_t *ina);
float INA219_GetShuntVoltage(INA219_t *ina);
float INA219_GetCurrent(INA219_t *ina);
float INA219_GetPower(INA219_t *ina);

#endif
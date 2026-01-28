#include "ina219.h"

/* Low-level I2C access */
static void INA219_WriteRegister(INA219_t *ina, uint8_t reg, uint16_t value)
{
    uint8_t data[2];
    data[0] = value >> 8;
    data[1] = value & 0xFF;

    HAL_I2C_Mem_Write(
        ina->hi2c,
        ina->addr,      
        reg,
        I2C_MEMADD_SIZE_8BIT,
        data,
        2,
        HAL_MAX_DELAY
    );
}

static uint16_t INA219_ReadRegister(INA219_t *ina, uint8_t reg)
{
    uint8_t data[2] = {0};
    HAL_I2C_Mem_Read(
        ina->hi2c,
        ina->addr,
        reg,
        I2C_MEMADD_SIZE_8BIT,
        data,
        2,
        HAL_MAX_DELAY
    );
    return (data[0] << 8) | data[1];
}

/* Inicializa struct e I2C */
void INA219_Init(INA219_t *ina, I2C_HandleTypeDef *hi2c, uint8_t addr)
{
    ina->hi2c = hi2c;
    ina->addr = addr;
    ina->currentLSB = 0.1f;  // 100 uA per bit
    ina->powerLSB   = 0.002f; // 2 mW per bit
}

/* Configuração típica 32V, 2A */
void INA219_SetCalibration32V2A(INA219_t *ina)
{
    // Formula de calibração do datasheet
    INA219_WriteRegister(ina, REG_CALIBRATION, 4096);
    INA219_WriteRegister(ina, REG_CONFIG,
                         (BUS_VOLTAGE_RANGE_32V << 13) |
                         (GAIN_DIV_8_320MV << 11) |
                         (ADC_RES_12BIT_1S << 7) |
                         (ADC_RES_12BIT_1S << 3) |
                         MODE_SANDBVOLT_CONTINUOUS);
}

/* Funções públicas de leitura */
float INA219_GetShuntVoltage(INA219_t *ina)
{
    int16_t raw = (int16_t)INA219_ReadRegister(ina, REG_SHUNTVOLTAGE);
    return raw * 0.01f; // 10uV per bit, exemplo
}

float INA219_GetBusVoltage(INA219_t *ina)
{
    uint16_t raw = INA219_ReadRegister(ina, REG_BUSVOLTAGE);
    return (raw >> 3) * 0.004f; // 4mV per bit, exemplo
}

float INA219_GetCurrent(INA219_t *ina)
{
    int16_t raw = (int16_t)INA219_ReadRegister(ina, REG_CURRENT);
    return raw * ina->currentLSB;
}

float INA219_GetPower(INA219_t *ina)
{
    uint16_t raw = INA219_ReadRegister(ina, REG_POWER);
    return raw * ina->powerLSB;
}
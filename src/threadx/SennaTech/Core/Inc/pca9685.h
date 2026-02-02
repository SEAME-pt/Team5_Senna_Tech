#ifndef PCA9685_H
#define PCA9685_H
#pragma once
#include <stdint.h>
#include "app_threadx.h"
/* I2C address (shifted for HAL) */
#define SERVO_ADDRESS     0x40 << 1
#define DC_ADDRESS     0x60 << 1

/* Registers */
#define MODE1               0x00
#define MODE2               0x01
#define PRESCALE            0xFE

#define LED0_ON_L            0x06
#define LED0_ON_H            0x07
#define LED0_OFF_L           0x08
#define LED0_OFF_H           0x09

#define ALL_LED_ON_L         0xFA
#define ALL_LED_ON_H         0xFB
#define ALL_LED_OFF_L        0xFC
#define ALL_LED_OFF_H        0xFD

/* Bits */
#define RESTART              0x80
#define SLEEP                0x10
#define ALLCALL              0x01
#define OUTDRV               0x04

typedef struct
{
    I2C_HandleTypeDef *hi2c;
    uint8_t address;
} PCA9685_t;

/* API */
void    PCA9685_Init(PCA9685_t *dev, I2C_HandleTypeDef *hi2c, uint8_t address);
void    PCA9685_SetPWMFreq(PCA9685_t *dev, uint16_t freq_hz);
void    PCA9685_SetPWM(PCA9685_t *dev, uint8_t channel, uint16_t on, uint16_t off);
void    PCA9685_SetAllPWM(PCA9685_t *dev, uint16_t on, uint16_t off);

/* Low level */
void    PCA9685_WriteByte(PCA9685_t *dev, uint8_t reg, uint8_t data);
uint8_t PCA9685_ReadByte(PCA9685_t *dev, uint8_t reg);

#endif

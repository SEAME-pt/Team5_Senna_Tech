#include "pca9685.h"

/*
** prescale = round(25MHz / (4096 * freq)) - 1
** versão inteira
*/
void PCA9685_SetPWMFreq(PCA9685_t *dev, uint8_t freq_hz)
{
    uint8_t oldmode = PCA9685_ReadByte(dev, MODE1);
    uint8_t sleep   = (oldmode & 0x7F) | SLEEP;

    PCA9685_WriteByte(dev, MODE1, sleep);
    PCA9685_WriteByte(dev, PRESCALE, freq_hz);
    PCA9685_WriteByte(dev, MODE1, oldmode);

    tx_sleep(1); // ~5ms
    PCA9685_WriteByte(dev, MODE1, oldmode | RESTART);
}

void PCA9685_Init(PCA9685_t *dev, void *hi2c, uint8_t address)
{
    dev->hi2c    = hi2c;
    dev->address = address;

    PCA9685_SetAllPWM(dev, 0, 0);
    PCA9685_WriteByte(dev, MODE2, OUTDRV);
    PCA9685_WriteByte(dev, MODE1, ALLCALL);

    tx_sleep(1); // ~5ms

    uint8_t mode1 = PCA9685_ReadByte(dev, MODE1);
    mode1 &= ~SLEEP;
    PCA9685_WriteByte(dev, MODE1, mode1);

    tx_sleep(1); // ~5ms
}

void PCA9685_SetPWM(PCA9685_t *dev, uint8_t channel, uint16_t on, uint16_t off)
{
    PCA9685_WriteByte(dev, LED0_ON_L  + 4 * channel, on & 0xFF);
    PCA9685_WriteByte(dev, LED0_ON_H  + 4 * channel, on >> 8);
    PCA9685_WriteByte(dev, LED0_OFF_L + 4 * channel, off & 0xFF);
    PCA9685_WriteByte(dev, LED0_OFF_H + 4 * channel, off >> 8);
}

void PCA9685_SetAllPWM(PCA9685_t *dev, uint16_t on, uint16_t off)
{
    PCA9685_WriteByte(dev, ALL_LED_ON_L,  on & 0xFF);
    PCA9685_WriteByte(dev, ALL_LED_ON_H,  on >> 8);
    PCA9685_WriteByte(dev, ALL_LED_OFF_L, off & 0xFF);
    PCA9685_WriteByte(dev, ALL_LED_OFF_H, off >> 8);
}

void PCA9685_WriteByte(PCA9685_t *dev, uint8_t reg, uint8_t data)
{
    I2C_WriteReg(dev->hi2c, dev->address, reg, data);
}

uint8_t PCA9685_ReadByte(PCA9685_t *dev, uint8_t reg)
{
    uint8_t data = 0;

    I2C_ReadReg(dev->hi2c, dev->address, reg, &data);

    return data;
}

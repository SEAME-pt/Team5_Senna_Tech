#include "../Inc/pca9685.h"

/*
** prescale = round(25MHz / (4096 * freq)) - 1
** versão inteira
*/
void PCA9685_SetPWMFreq(PCA9685_t *dev, uint16_t freq_hz)
{
    uint32_t prescale;

    if (freq_hz < 1)
        freq_hz = 1;

    prescale = 25000000UL;
    prescale /= 4096UL;
    prescale /= freq_hz;
    prescale -= 1;

    if (prescale > 255)
        prescale = 255;

    uint8_t oldmode = PCA9685_ReadByte(dev, MODE1);
    uint8_t sleep   = (oldmode & 0x7F) | SLEEP;

    PCA9685_WriteByte(dev, MODE1, sleep);
    PCA9685_WriteByte(dev, PRESCALE, (uint8_t)prescale);
    PCA9685_WriteByte(dev, MODE1, oldmode);

    tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND / 200); // ~5ms
    PCA9685_WriteByte(dev, MODE1, oldmode | RESTART);
}

void PCA9685_Init(PCA9685_t *dev, I2C_HandleTypeDef *hi2c, uint8_t address)
{
    dev->hi2c    = hi2c;
    dev->address = address;

    PCA9685_SetAllPWM(dev, 0, 0);
    PCA9685_WriteByte(dev, MODE2, OUTDRV);
    PCA9685_WriteByte(dev, MODE1, ALLCALL);

    tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND / 200); // ~5ms

    uint8_t mode1 = PCA9685_ReadByte(dev, MODE1);
    mode1 &= ~SLEEP;
    PCA9685_WriteByte(dev, MODE1, mode1);

    tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND / 200); // ~5ms
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
    HAL_I2C_Mem_Write(
        dev->hi2c,
        dev->address,
        reg,
        I2C_MEMADD_SIZE_8BIT,
        &data,
        1,
        HAL_MAX_DELAY
    );
}

uint8_t PCA9685_ReadByte(PCA9685_t *dev, uint8_t reg)
{
    uint8_t data = 0;

    HAL_I2C_Mem_Read(
        dev->hi2c,
        dev->address,
        reg,
        I2C_MEMADD_SIZE_8BIT,
        &data,
        1,
        HAL_MAX_DELAY
    );

    return data;
}

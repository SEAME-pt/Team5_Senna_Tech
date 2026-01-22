#include "car.h"
#include <math.h>

static float duty_from_percent_50hz(float value)
{
    return 0.0015f + (value * 0.001f); // seconds
}

void car_init(car_t *car, I2C_HandleTypeDef *hi2c)
{
    PCA9685_Init(&car->steering, hi2c, SERVO_ADDRESS);
    PCA9685_Init(&car->throttle, hi2c, DC_ADDRESS);

    PCA9685_SetPWMFreq(&car->steering, PWM_FREQ_50HZ);
    PCA9685_SetPWMFreq(&car->throttle, PWM_FREQ_50HZ);

    car_set_steering_percent(car, 0.0f);
    car_set_throttle_percent(car, 0.0f);

    tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND);
}

void car_set_steering_percent(car_t *car, float percent)
{
    float pulse = duty_from_percent_50hz(-percent);
    uint16_t raw = (uint16_t)(pulse * PWM_FREQ_50HZ * 4096.0f);

    PCA9685_SetPWM(&car->steering, PWM_STEERING_CHANNEL, 0, raw);
}

void car_set_throttle_percent(car_t *car, float percent)
{
    uint16_t pwm = (uint16_t)(fabsf(percent) * PWM_MAX_RAW_VALUE);

    if (percent > 0.0f)
    {
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1,  0, PWM_MAX_RAW_VALUE);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2,  0, 0);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1, 0, 0);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2, 0, PWM_MAX_RAW_VALUE);
    }
    else
    {
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1,  0, 0);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2,  0, PWM_MAX_RAW_VALUE);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1, 0, PWM_MAX_RAW_VALUE);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2, 0, 0);
    }

    PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_PWM,  0, pwm);
    PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_PWM, 0, pwm);
}

/* float car_get_battery_voltage(car_t *car)
{
    return INA219_GetBusVoltage(&car->battery) +
           INA219_GetShuntVoltage(&car->battery);
}

float car_get_battery_current(car_t *car)
{
    return INA219_GetCurrent(&car->battery);
}

float car_get_battery_power(car_t *car)
{
    return INA219_GetPower(&car->battery);
} */
#include "car.h"
#include <math.h>

static float duty_from_percent_50hz(float value)
{
    return 0.0015f + (value * 0.001f);
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
    float dutyCycle = duty_from_percent_50hz(-percent);
    int raw = (int)(PWM_MAX_RAW_VALUE * (dutyCycle / PWM_WAVELENGTH_50HZ));

    PCA9685_SetPWM(&car->steering, PWM_STEERING_CHANNEL, 0, raw);
}

void car_set_throttle_percent(car_t *car, float percent)
{

    if (percent > 0.0f)
    {
        // Frente
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1,  0, PWM_MAX_RAW_VALUE);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2,  0, 0);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1, 0, 0);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2, 0, PWM_MAX_RAW_VALUE);
    }
    else if (percent < 0.0f)
    {
        // Ré
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1,  0, 0);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2,  0, PWM_MAX_RAW_VALUE);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1, 0, PWM_MAX_RAW_VALUE);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2, 0, 0);
    }
    else
    {
        // Stop
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1,  0, 0);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2,  0, 0);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1, 0, 0);
        PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2, 0, 0);
    }

    int pwm = PWM_MAX_RAW_VALUE * fabs(percent);
    // Aplica PWM proporcional
    PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_PWM,  0, pwm);
    PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_PWM, 0, pwm);
}
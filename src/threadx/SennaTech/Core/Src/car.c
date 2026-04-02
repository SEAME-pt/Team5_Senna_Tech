#include "car.h"
#include <math.h>

float duty_from_percent_50hz(float value)
{
    return 0.0015f + (value * 0.001f);
}

void car_init(car_t *car, void *hi2c)
{
    PCA9685_Init(&car->steering, hi2c, SERVO_ADDRESS);
    PCA9685_Init(&car->throttle, hi2c, DC_ADDRESS);

    PCA9685_SetPWMFreq(&car->steering, PWM_FREQ_50HZ);
    PCA9685_SetPWMFreq(&car->throttle, PWM_FREQ_50HZ);

    car_set_steering_percent(car, 0.0f);
    car_set_throttle_percent(car, 0.0f);

    tx_sleep(1);
}

int calculateRaw(float percent)
{
    percent *= -1.0;

    if (percent > 1.0f) percent = 1.0f;
    if (percent < -1.0f) percent = -1.0f;

    int raw = SERVO_RAW_MIN +
              (int)((percent + 1.0f) * 0.5f *
              (SERVO_RAW_MAX - SERVO_RAW_MIN));
    
    if (raw > SERVO_RAW_MAX)
        raw = SERVO_RAW_MAX;
    if (raw < SERVO_RAW_MIN)
        raw = SERVO_RAW_MIN;
    return raw;
}

void car_set_steering_percent(car_t *car, float percent)
{
    percent *= -1.0;

    if (percent > 1.0f) percent = 1.0f;
    if (percent < -1.0f) percent = -1.0f;

    int raw = SERVO_RAW_MIN +
              (int)((percent + 1.0f) * 0.5f *
              (SERVO_RAW_MAX - SERVO_RAW_MIN));
    
    if (raw > SERVO_RAW_MAX)
        raw = SERVO_RAW_MAX;
    if (raw < SERVO_RAW_MIN)
        raw = SERVO_RAW_MIN;
    //log_debug("raw: %i", raw);
    PCA9685_SetPWM(&car->steering, PWM_STEERING_CHANNEL, 0, raw);
}

void car_set_throttle_percent(car_t *car, float percent)
{
    if (percent > 100.0f)
        percent = 100.0f;
    if (percent < -100.0f)
        percent = -100.0f;

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

    int pwm = (int)((float)PWM_MAX_RAW_VALUE * (fabs(percent) / 100.0f));
    if (pwm > PWM_MAX_RAW_VALUE)
        pwm = PWM_MAX_RAW_VALUE; // ALTERAR NO CODIGO ORIGINAL!!
    // Aplica PWM proporcional
    PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_PWM,  0, pwm);
    PCA9685_SetPWM(&car->throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_PWM, 0, pwm);
}
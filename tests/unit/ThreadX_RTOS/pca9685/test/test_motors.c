#include "unity.h"
#include "mock_i2c_hal.h"
#include "mock_sleep_hal.h"
#include "mock_pca9685.h"
#include "car.h"

car_t car;

// CAR INIT TEST
void test_car_init(void)
{
    void *i2c = NULL;

    PCA9685_Init_Expect(&car.steering, i2c, SERVO_ADDRESS);
    PCA9685_Init_Expect(&car.throttle, i2c, DC_ADDRESS);

    PCA9685_SetPWMFreq_Expect(&car.steering, PWM_FREQ_50HZ);
    PCA9685_SetPWMFreq_Expect(&car.throttle, PWM_FREQ_MOTOR_HZ);

    PCA9685_SetPWM_Ignore();

    tx_sleep_Expect(1);

    car_init(&car, i2c);
}


// THROTTLE 50% SPEED FORWARD TEST
void    test_car_throttle_half_forward(void)
{

    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1,  0, PWM_MAX_RAW_VALUE);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2,  0, 0);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1, 0, 0);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2, 0, PWM_MAX_RAW_VALUE);
    
    int pwm = PWM_MAX_RAW_VALUE * fabs(0.5f);

    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_PWM,  0, pwm);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_PWM, 0, pwm);

    car_set_throttle_percent(&car, 0.5f);
}

// THROTTLE 100% SPEED FORWARD TEST
void    test_car_throttle_max_forward(void)
{

    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1,  0, PWM_MAX_RAW_VALUE);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2,  0, 0);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1, 0, 0);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2, 0, PWM_MAX_RAW_VALUE);
    
    int pwm = PWM_MAX_RAW_VALUE * fabs(1.0f);

    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_PWM,  0, pwm);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_PWM, 0, pwm);

    car_set_throttle_percent(&car, 1.0f);
}

// THROTTLE OVERFLOW SPEED FORWARD TEST
void    test_car_throttle_overflow_forward(void)
{
    // PRECISO CORRIGIR ISTO NO CÓDIGO PARA PROTEGER O DC
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1,  0, PWM_MAX_RAW_VALUE);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2,  0, 0);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1, 0, 0);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2, 0, PWM_MAX_RAW_VALUE);
    
    int pwm = PWM_MAX_RAW_VALUE * fabs(1.0f);

    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_PWM,  0, pwm);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_PWM, 0, pwm);

    car_set_throttle_percent(&car, 1.1f);
}


// THROTTLE 50% SPEED BACK TEST
void    test_car_throttle_half_back(void)
{

    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1,  0, 0);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2,  0, PWM_MAX_RAW_VALUE);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1, 0, PWM_MAX_RAW_VALUE);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2, 0, 0);
    
    int pwm = PWM_MAX_RAW_VALUE * fabs(-0.5f);

    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_PWM,  0, pwm);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_PWM, 0, pwm);

    car_set_throttle_percent(&car, -0.5f);
}

// THROTTLE 100% SPEED BACK TEST
void    test_car_throttle_max_back(void)
{

    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1,  0, 0);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2,  0, PWM_MAX_RAW_VALUE);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1, 0, PWM_MAX_RAW_VALUE);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2, 0, 0);
    
    int pwm = PWM_MAX_RAW_VALUE * fabs(-1.0f);

    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_PWM,  0, pwm);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_PWM, 0, pwm);

    car_set_throttle_percent(&car, -1.0f);
}

// THROTTLE OVERFLOW SPEED BACK TEST
void    test_car_throttle_overflow_back(void)
{

    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1,  0, 0);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2,  0, PWM_MAX_RAW_VALUE);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1, 0, PWM_MAX_RAW_VALUE);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2, 0, 0);
    
    int pwm = PWM_MAX_RAW_VALUE * fabs(-1.0f);

    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_PWM,  0, pwm);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_PWM, 0, pwm);

    car_set_throttle_percent(&car, -1.1f);
}

// STOP CAR
void    test_car_throttle_stop(void)
{

    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1,  0, 0);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2,  0, 0);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1, 0, 0);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2, 0, 0);
    
    int pwm = PWM_MAX_RAW_VALUE * fabs(0.0f);

    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_PWM,  0, pwm);
    PCA9685_SetPWM_Expect(&car.throttle, PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_PWM, 0, pwm);

    car_set_throttle_percent(&car, 0.0f);
}


// TURN LEFT 50%
void test_car_steering_half_left(void)
{
    float percent = 0.5f;

    int raw = calculateRaw(percent);
    PCA9685_SetPWM_Expect(&car.steering, PWM_STEERING_CHANNEL, 0, raw);

    car_set_steering_percent(&car, 0.5f);
}

// TURN LEFT 100%
void test_car_steering_full_left(void)
{
    float percent = 1.0f;
    
    int raw = calculateRaw(percent);
    PCA9685_SetPWM_Expect(&car.steering, PWM_STEERING_CHANNEL, 0, raw);
    
    car_set_steering_percent(&car, 1.0f);
}

// TURN RIGHT 50%
void test_car_steering_half_right(void)
{
    float percent = -0.5f;

    int raw = calculateRaw(percent);
    PCA9685_SetPWM_Expect(&car.steering, PWM_STEERING_CHANNEL, 0, raw);
    
    car_set_steering_percent(&car, -0.5f);
}

// TURN RIGHT 100%
void test_car_steering_full_right(void)
{
    float percent = -1.0f;
    
    int raw = calculateRaw(percent);
    PCA9685_SetPWM_Expect(&car.steering, PWM_STEERING_CHANNEL, 0, raw);
    
    car_set_steering_percent(&car, -1.0f);
}

// STEERING STOP
void test_car_steering_stop(void)
{
    float percent = 0.0f;
    
    int raw = calculateRaw(percent);
    PCA9685_SetPWM_Expect(&car.steering, PWM_STEERING_CHANNEL, 0, raw);
    
    car_set_steering_percent(&car, 0.0f);
}

// OVERFLOW LEFT
void test_car_steering_overflow_left(void)
{
    float percent = 1.0f;

    int raw = calculateRaw(percent);
    PCA9685_SetPWM_Expect(&car.steering, PWM_STEERING_CHANNEL, 0, raw);

    car_set_steering_percent(&car, 1.1f);
}

// OVERFLOW RIGHT
void test_car_steering_overflow_right(void)
{
    float percent = -1.0f;
    
    int raw = calculateRaw(percent);
    PCA9685_SetPWM_Expect(&car.steering, PWM_STEERING_CHANNEL, 0, raw);
    
    car_set_steering_percent(&car, -1.1f);
}


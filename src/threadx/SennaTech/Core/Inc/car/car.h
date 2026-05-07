#ifndef CAR_H
#define CAR_H

#include "pca9685.h"
#include <math.h>

#define PWM_RESOLUTION 12
#define PWM_MAX_RAW_VALUE ((1 << PWM_RESOLUTION) - 1)  
#define PWM_FREQ_SERVO_HZ 0x79
#define PWM_FREQ_MOTOR_HZ 0x05
#define PWM_STEERING_CHANNEL 0
#define PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1 5
#define PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2 6
#define PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_PWM 7
#define PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1 1
#define PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2 2
#define PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_PWM 0

/* Full mechanical range (avoid - causes stall) */
#define SERVO_RAW_MIN_MECH 205
#define SERVO_RAW_MAX_MECH 410

#define SERVO_RAW_MIN 215
#define SERVO_RAW_MAX 400

typedef struct
{
    PCA9685_t steering;
    PCA9685_t throttle;
} car_t;

void car_init(car_t *car, void *hi2c);
void car_set_steering_percent(car_t *car, float percent);
void car_set_throttle_percent(car_t *car, float percent, uint8_t brake);
int  calculateRaw(float percent);

#endif
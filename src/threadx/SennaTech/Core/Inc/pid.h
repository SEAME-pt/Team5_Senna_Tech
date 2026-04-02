#ifndef PID_H
#define PID_H

#include <stdint.h>

typedef struct
{
    float kp;
    float ki;
    float kd;
    float prev_error;
    float integral;
    float integral_limit;
    float output_limit;
} pid_t;

void pid_init(pid_t *pid, float kp, float ki, float kd);
float pid_update(pid_t *pid, float target, float current, float dt);
void pid_reset(pid_t *pid);
void pid_set_integral_limit(pid_t *pid, float limit);
void pid_set_output_limit(pid_t *pid, float limit);

#endif
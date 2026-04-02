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

/*

Proportional gain -> reacts to current error
Integral gain -> reacts to accumulated error over time
Derivative gain -> reacts to the rate of change of error

Slow to respond: increase Kp.
Never reaches the target (steady-state error): increase Ki.
Overshoots the target a lot: increase Kd or reduce Kp.
Continuous oscillation: reduce Kp and/or Ki.
Output jitter (noise): reduce Kd.
*/
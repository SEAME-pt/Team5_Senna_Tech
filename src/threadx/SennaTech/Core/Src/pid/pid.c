#include "pid.h"

void pid_init(pid_t *pid, float kp, float ki, float kd)
{
    pid->kp = kp;
    pid->ki = ki;
    pid->kd = kd;
    pid->prev_error = 0.0f;
    pid->integral = 0.0f;
    pid->integral_limit = 1.0f;
    pid->output_limit = 1.0f;
}

float pid_update(pid_t *pid, float target, float current, float dt)
{
    if (dt <= 0.0f)
        return 0.0f;

    const float error = target - current;
    const float proportional = pid->kp * error;

    pid->integral += error * dt;
    pid->integral = clamp_symmetric(pid->integral, pid->integral_limit);

    const float integral = pid->ki * pid->integral;
    const float derivative = pid->kd * ((error - pid->prev_error) / dt);

    pid->prev_error = error;

    return clamp_symmetric(proportional + integral + derivative, pid->output_limit);
}

void pid_reset(pid_t *pid)
{
    pid->prev_error = 0.0f;
    pid->integral = 0.0f;
}

void pid_set_integral_limit(pid_t *pid, float limit)
{
    pid->integral_limit = absf_local(limit);
    pid->integral = clamp_symmetric(pid->integral, pid->integral_limit);
}

void pid_set_output_limit(pid_t *pid, float limit)
{
    pid->output_limit = absf_local(limit);
}
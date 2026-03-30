#include "PID.hpp"

double mapPIDtoServo(double pid_value, double min_angle, double max_angle) {

    // Clamp pid_value to [-1, 1]
    if (pid_value > 1.0) pid_value = 1.0;
    if (pid_value < -1.0) pid_value = -1.0;

    double servo_angle = (pid_value + 1.0) * (max_angle - min_angle) / 2.0 + min_angle;

    return (servo_angle);
}

static double clampSymmetric(double value, double limit) {

    if (limit <= 0.0)
        return 0.0;
	else if (value > limit)
        return limit;
    else if (value < -limit)
        return -limit;

    return value;
}

PID::PID(double kp, double ki, double kd)
    : _kp(kp),
      _ki(ki),
      _kd(kd),
      _prevError(0.0),
      _integral(0.0),
      _integralLimit(1.0),
      _outputLimit(1.0) {}

PID::~PID() {}

double PID::update(double target, double current, double dt) {

    if (dt <= 0.0)
        return 0.0;

    const double error = target - current;
    const double proportional = _kp * error;

    _integral += error * dt;
    _integral = clampSymmetric(_integral, _integralLimit);

    const double integral = _ki * _integral;
    const double derivative = _kd * ((error - _prevError) / dt);

    _prevError = error;

    const double output = proportional + integral + derivative;
    return clampSymmetric(output, _outputLimit);
}

void PID::reset() {
    _prevError = 0.0;
    _integral = 0.0;
}

void PID::setIntegralLimit(double limit) {
    _integralLimit = std::abs(limit);
    _integral = clampSymmetric(_integral, _integralLimit);
}

void PID::setOutputLimit(double limit) {
    _outputLimit = std::abs(limit);
}

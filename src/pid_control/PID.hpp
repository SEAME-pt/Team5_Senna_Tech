#pragma once

#include <cmath>

class PID {

public:
    PID(double kp, double ki, double kd);
	~PID();

    double	update(double target, double current, double dt);

	// Reset internal state (integral accumulator and previous error).
    void	reset();

	void	setIntegralLimit(double limit);
    void	setOutputLimit(double limit);

private:

	// This controls how strongly the controller reacts to the current error.
    double	_kp;		// proportional gain

	// This controls how much past error accumulates over time.
    double	_ki;		// integral gain

	// This controls how strongly the controller reacts to changes in error.
    double	_kd;		// derivative gain

	// Internal state
    double	_prevError;
    double	_integral;

    double	_integralLimit;
    double	_outputLimit;
};


/*
common examples of instantiating this object to steering values:

kp = 0.3 – 0.6
ki = 0.0 – 0.02
kd = 0.05 – 0.15
*/
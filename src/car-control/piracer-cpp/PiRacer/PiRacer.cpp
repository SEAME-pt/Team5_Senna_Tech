#include <cmath>
#include "PiRacer.hpp"

PiRacer::PiRacer():
	_steeringController(PCA9685(1, 0x40)),
	_throttleController(PCA9685(1, 0x60)),
	_batteryMonitor(INA219(1, 0x41))
{
	_steeringController.setPWMFreq(PWM_FREQ_50HZ);
	_throttleController.setPWMFreq(PWM_FREQ_50HZ);
	_warmUP();
}

PiRacer::~PiRacer(){}

void PiRacer::_warmUP()
{
	setSteeringPercent(0.0);
	setThrottlePercent(0.0);
	sleep(1);
}

float PiRacer::_get50HzDutyCycleFromPercent(float value)
{
	return 0.0015 + (value * 0.001);
}

float PiRacer::getBatteryVoltage()
{
	return _batteryMonitor.getBusVoltage() + _batteryMonitor.getShuntVoltage();
}

float PiRacer::getBatteryCurrent()
{
	return _batteryMonitor.getCurrent();
}

float PiRacer::getPowerConsumption()
{
	return _batteryMonitor.getPower();
}

void PiRacer::setSteeringPercent(float percent)
{
	float dutyCycle = _get50HzDutyCycleFromPercent(-percent);
	int rawValue = static_cast<int>(PWM_MAX_RAW_VALUE * (dutyCycle / PWM_WAVELENGTH_50HZ));
	_steeringController.setPWM(PWM_STEERING_CHANNEL, 0, rawValue);
}

void PiRacer::setThrottlePercent(float percent)
{
	if (percent > 0)
	{
		_throttleController.setPWM(PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1, 0, PWM_MAX_RAW_VALUE);
		_throttleController.setPWM(PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2, 0, 0);
		_throttleController.setPWM(PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1, 0, 0);
		_throttleController.setPWM(PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2, 0, PWM_MAX_RAW_VALUE);
	}
	else
	{
		_throttleController.setPWM(PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_1, 0, 0);
		_throttleController.setPWM(PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_2, 0, PWM_MAX_RAW_VALUE);
		_throttleController.setPWM(PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_1, 0, PWM_MAX_RAW_VALUE);
		_throttleController.setPWM(PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_2, 0, 0);
	}

	int pwmRawValue = PWM_MAX_RAW_VALUE * std::abs(percent);
	_throttleController.setPWM(PWM_THROTTLE_CHANNEL_LEFT_MOTOR_IN_PWM, 0, pwmRawValue);
	_throttleController.setPWM(PWM_THROTTLE_CHANNEL_RIGHT_MOTOR_IN_PWM, 0, pwmRawValue);
}

void	PiRacer::printEnergyReport() {
		float voltage = this->getBatteryVoltage();
		float current = this->getBatteryCurrent();
		float power = this->getPowerConsumption();
		std::cout << "Battery "
				<< "Voltage: " << voltage
				<< ", Current: " << current
				<< ", Power: " << power
				<< std::endl;
}
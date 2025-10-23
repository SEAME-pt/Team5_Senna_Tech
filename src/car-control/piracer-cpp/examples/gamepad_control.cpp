#include "../PiRacer/PiRacer.hpp"
#include "../Gamepad/ShanwanGamepad.hpp"

int main()
{
	// Ensure GPIO is initialized
/* 	if (gpioInitialise() < 0)
	{
		std::cerr << "pigpio initialization failed" << std::endl;
		return 1;
	}
	atexit(gpioTerminate); */

	// Create instances
	PiRacer racer;
	ShanWanGamepad gamepad;

	while (true)
	{
		ShanWanGamepadInput input = gamepad.read_data();

		float steering = input.analog_stick_right.x;
		float throttle = input.analog_stick_left.y;
		
		std::cout << "Throttle: " << throttle
				<< ", Steering: " << steering
				<< std::endl;
		racer.printEnergyReport();


		
		racer.setSteeringPercent(steering);
		racer.setThrottlePercent(throttle);
	}

	return 0;
}
#include "../PiRacer/PiRacer.hpp"

int main()
{
	// Ensure GPIO is initialized
/* 	if (gpioInitialise() < 0)
	{
		std::cerr << "pigpio initialization failed" << std::endl;
		return 1;
	} */

	// Create PiRacer Instance
	PiRacer racer;

	racer.setThrottlePercent(0.0);


	
	
	return 0;
}
#include "../PiRacer/PiRacer.hpp"
#include <iostream>

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

	std::cout << "Powertrain off" << std::endl;
	racer.printEnergyReport();
	sleep(1);

	std::cout << "Powertrain at 30%" << std::endl;
	racer.setThrottlePercent(0.3);
	sleep(3);
	racer.printEnergyReport();

	std::cout << "Powertrain at 100%" << std::endl;
	racer.setThrottlePercent(1.0);
	sleep(3);
	racer.printEnergyReport();

	std::cout << "Powertrain off" << std::endl;
	racer.setThrottlePercent(0.0);
	sleep(3);
	racer.printEnergyReport();

	// gpioTerminate();
	return 0;
}
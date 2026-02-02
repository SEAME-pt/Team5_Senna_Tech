#include "../PiRacer/PiRacer.hpp"
#include <iostream>

int main()
{
	// BATTERY READER TESTS
	PiRacer racer;

	std::cout << "Battery Percentage: " << racer.getBatteryPercentage() << "%" << std::endl;
	std::cout << "Battery Reloading: " << racer.isCharging() << std::endl;
	racer.printEnergyReport();
/* 	std::cout << "Powertrain off" << std::endl;
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
	racer.printEnergyReport(); */

	return 0;
}
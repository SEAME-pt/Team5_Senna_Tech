#include "../PiRacer/PiRacer.hpp"

int main()
{
	PiRacer racer;

	// THIS MAIN IS PROVIDED TO TEST THE MOTORS!

	racer.setThrottlePercent(0.0); // BETWEEN -1.0 AND +1.0
	racer.setSteeringPercent(0.0); // BETWEEN -1.0 AND +1.0
	
	return 0;
}
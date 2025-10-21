# PiRacer CPP
The goal of this project is to implement PiRacer-py project in cpp so that no python is needed to develop PiRacer applications. Not every feature from the original project is implemented yet, but everything necessary for controlling the vehicle is there for you.

# Install
Tested device:
- Raspberry Pi 4 Model B
- Waveshare PiRacer AI Kit

Tested distribution:
- Raspberry Pi OS "Bullseye" (64-Bit)

### Install dependencies
```
sudo apt update
sudo apt install \
	pigpio \
	build-essentials \
	cmake
```

### Enable I2C
Use `raspi-config` tool to enable I2C:
```
sudo raspi-config
```
- Interface Options > I2C > Enable

Afterwards, reboot:
```
sudo reboot
```

# Examples
The following examples will show the basic functionality of PiRacer

## forward_backward_left_right
Basic example code for testing steers and throttle
```
int main()
{
	...

	// Create PiRacer Instance
	PiRacer racer;

	// Forward
	racer.setThrottlePercent(0.2);
	sleep(2);

	// Backward
	racer.setThrottlePercent(-0.2);
	sleep(2);

	// Steering Left
	racer.setSteeringPercent(1.0);
	sleep(1);

	// Steering Right
	racer.setSteeringPercent(-1.0);
	sleep(1);
	
	...
}
```

## gamepad_control
Read inputs from the gamepad and control the vehicle.
```
int main()
{
	// Create instances
	PiRacer racer;
	ShanWanGamepad gamepad;

	while (true)
	{
		// Read inputs from gamepad
		ShanWanGamepadInput input = gamepad.read_data();

		float steering = input.analog_stick_left.x;
		float throttle = input.analog_stick_right.y * 0.5; // limit throtle to 50%
		
		racer.setSteeringPercent(steering);
		racer.setThrottlePercent(throttle);
	}
}
```
Also it is possible to create gamepad instance with non-blocking mode like:
```
// set non-blocking flag to true
ShanWanGamepad gamepad("/dev/input/js0", true);
```

## read_battery
Read battery status from the vehicle
```
int main()
{
	// Create PiRacer Instance
	PiRacer racer;

	float voltage = racer.getBatteryVoltage();
	float current = racer.getBatteryCurrent();
	float power = racer.getPowerConsumption();
	std::cout << "Battery "
			<< "Voltage: " << voltage
			<< ", Current: " << current
			<< ", Power: " << power
			<< std::endl;

	...
}
```

## Building examples
Run follwing commands to build above examples:
```
mkdir build
cd build
cmake ..
make
```

pigpio library requires root permission to control gpio pins. So run example programs with `sudo`
```
sudo ./forward_backward_left_right
```

> Keep in mind that to use gpio `gpioInitialise()` must be called in your program before using piracer instance. And when terminating the program, call `gpioTerminate()`

# References
[Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)

[pigpio](https://github.com/joan2937/pigpio)

[Waveshare PiRacer AI Kit](https://www.waveshare.com/wiki/PiRacer_AI_Kit)

[PiRacer-py](https://github.com/twyleg/piracer_py)

[Adafruit_INA219](https://github.com/adafruit/Adafruit_CircuitPython_INA219)

[Adafruit_PCA9685](https://github.com/adafruit/Adafruit_CircuitPython_PCA9685)
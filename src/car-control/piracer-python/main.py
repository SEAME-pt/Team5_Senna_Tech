"""
main.py — Nvidia JetRacer car control using a joystick

This script performs the following steps:
1. Initializes the car and the joystick.
2. Continuously reads joystick axes.
3. Applies throttle and steering values to the car.
4. Prints the current values to the console for debugging.
5. Ensures safe shutdown of the car on exit.
"""

from jetracer.nvidia_racecar import NvidiaRacecar
import pygame
import time

car = NvidiaRacecar() # Create an instance of the JetRacer car

pygame.init()  # Initialize the main pygame module
pygame.joystick.init()  # Initialize the joystick module

# Check if any joystick is connected to the Raspberry Pi
if pygame.joystick.get_count() == 0:
    print("No joystick connected!")
    exit(1)  # Exit the program if no joystick is detected

# Select the first connected joystick and initialize it
joystick = pygame.joystick.Joystick(0)
joystick.init()

car.throttle_gain = 1  # Gain factor for throttle (acceleration)
car.steering_gain = 1  # Gain factor for steering (direction)
car.steering_offset = 0  # Steering servo offset adjustment

try:
    while True:
        # Update pygame events (required for reading joystick input)
        pygame.event.pump()

        # axis 1: throttle (forward/backward)
        # axis 2: steering (left/right)
        throttle_axis = joystick.get_axis(1)
        steering_axis = joystick.get_axis(2)

        # Apply throttle value, multiplying by the gain
        # Note: joystick axis usually ranges from -1 (up) to 1 (down)
        car.throttle = throttle_axis * car.throttle_gain

        # Apply steering value, multiplying by the gain
        car.steering = steering_axis * car.steering_gain

        # Print current values to the console for debugging
        print(f"Throttle: {car.throttle:.2f}, Steering: {car.steering:.2f}")

        # Small delay to avoid overloading the CPU
        time.sleep(0.05)

# Handle user interruption (Ctrl+C)
except KeyboardInterrupt:
    print("\nExiting...")

# Safe shutdown
finally:
    # Set throttle and steering to zero to safely stop the car
    car.throttle = 0
    car.steering = 0

    # Quit joystick and pygame modules
    pygame.joystick.quit()
    pygame.quit()


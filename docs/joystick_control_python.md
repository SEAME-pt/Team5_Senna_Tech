# main.py 🚗

### Introduction

- A structured explanation of how main.py works and control the car by joystick
- It reads the joystick's analog axes to send the commands.


### Important consideration

- Even though we are working with a PiRacer (Raspberry Pi 5), we decided to use the code developed for the JetRacer solely to understand how acceleration and steering commands (throttle and steering) are sent.

### 🚀 Execution

```bash
python3 main.py
```

### 📦 Dependencies

`jetracer` (Nvidia official library)

`pygame` (pygame is a Python library primarily used for creating games, in this script is useful to respond the joystick). [Check Pygame Documentation here!](https://www.pygame.org/docs/) 

### ⚙️ Exploring the code


| Variable          | Description                                                                  |
| ----------------- | ---------------------------------------------------------------------------- |
| `car`             | Controllable instance of the JetRacer                                        |
| `throttle_axis`   | Value of the throttle axis read from the joystick                            |
| `steering_axis`   | Value of the steering axis read from the joystick                            |
| `throttle_gain`   | Factor that amplifies or reduces the throttle response                       |
| `steering_gain`   | Factor that amplifies or reduces the steering response                       |
| `steering_offset` | Corrects the steering alignment (if the car does not go straight at neutral) |
| `joystick`        | Object representing the connected joystick                                   |
                               
#### Connecting the joystick

```python
pygame.init() #initialize the pygame 
pygame.joystick.init() #initialize the joystick module

# Check if any joystick is connected to the Raspberry Pi
if pygame.joystick.get_count() == 0:
    print("No joystick connected!")
    exit(1)  # Exit the program if no joystick is detected

# Select the first connected joystick and initialize it
joystick = pygame.joystick.Joystick(0)
joystick.init()
```

#### Loop

- The loop continuously reads the joystick axes, applies the gain factors, and updates the car's throttle and steering in real time.

```python
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
```
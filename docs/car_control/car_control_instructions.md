# Joystick Car Control

This guide explains how to control the car with the joystick after connecting to the Raspberry Pi 5.

## Execution

1. Connect to the Raspberry Pi 5 through SSH.
2. Go to the directory where the control executable is located (/home).
3. Run:

```bash
./control
```

After the program starts, the joystick can send throttle and steering commands over CAN, depending on the selected mode.

## Available modes

### Autonomous mode (`0`) - button `A`

- Joystick commands are ignored and are not sent through CAN.
- The microcontroller remains available to receive commands on the same CAN IDs.
- In this mode, commands must come from another source, such as the AI model, not from the joystick.

### Manual mode (`1`) - button `Y`

- All joystick commands are accepted and sent to the microcontroller.
- Use this mode when the joystick should have full control of the car.
- If the AI model also sends commands at the same time, undefined behavior may occur.

### Debug mode (`2`) - button `B`

- Joystick throttle is accepted and sent to the microcontroller.
- Joystick steering is ignored.
- This mode is useful when steering is being tested from the AI model while throttle is still controlled by the joystick.

## Notes

- Make sure the joystick is connected before starting the executable.
- Confirm the correct mode before driving the car.
- Avoid sending commands from both the joystick and the AI model unless that behavior is intentional.

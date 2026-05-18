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

- Joystick commands are ignored; all drive commands come from the AI model.
- If the joystick is moved beyond the deadzone while in this mode, the car automatically switches to Manual mode.

### Manual mode (`1`) - button `Y`

- All joystick commands are accepted and sent to the microcontroller.
- This is the default mode when the program starts.
- Moving the joystick while in Autonomous mode will override it and return to Manual.

## Mode switching

- The car always starts in **Manual mode**.
- Pressing **A** switches to Autonomous mode, handing control to the AI model.
- Moving the joystick while in Autonomous mode **automatically overrides** back to Manual, without needing to press any button.

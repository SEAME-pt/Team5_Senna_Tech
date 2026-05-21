# Joystick Car Control

This guide explains how to control the car with the joystick after connecting to the Raspberry Pi 5.

---

## Programs

### `./control` — Joystick Controller

The main executable that reads joystick input and sends throttle and steering commands over CAN, depending on the active mode.

**Execution:**
1. Connect to the Raspberry Pi 5 through SSH.
2. Navigate to the directory where the executable is located (`/home`).
3. Run:
```bash
./control
```

### `run.py` — AI Autonomous Mode

A Python script that activates the full autonomous pipeline. When launched, it starts both `./control` and the AI model pipeline together. The joystick behaves exactly the same as when running `./control` directly — all mode logic, overrides, and button mappings still apply.

**Execution:**
```bash
python3 run.py
```

---

## Available Modes

### Manual Mode (`1`) — highest priority
- All joystick commands are accepted and sent to the microcontroller.
- This is the **default mode** when any program starts.
- **Moving any joystick axis immediately switches to Manual mode**, regardless of the current mode. Manual mode always takes priority.

### Autonomous Mode (`0`) — button `A`
- Joystick commands are ignored; all drive commands come from the AI model.
- Press **A** to enter this mode.
- Moving any joystick axis **instantly overrides** Autonomous mode and returns to Manual — no button press needed.

---

## Mode Switching Summary

| Trigger | Result |
|---|---|
| Program start | Manual mode |
| Press **A** | Switch to Autonomous mode |
| Move any joystick axis | Always switches to Manual mode (highest priority) |
| Press **Y** | Send parking system signal |

---

## Button Reference

| Button | Action |
|---|---|
| **A** | Activate Autonomous mode |
| **Y** | Send parking system signal |

import subprocess
import signal
import sys
import os
import socket
import struct
from time import sleep


ENABLE_DRIVE_CAN_ID = 0x003
DRIVE_COMMAND_CAN_ID = 0x001
CAN_INTERFACE = "can0"


def send_can_native(can_id, data, interface=CAN_INTERFACE):
    """Send a CAN message using native Linux SocketCAN."""

    can_frame_format = "=IB3x8s"

    try:
        s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        s.bind((interface,))

        if isinstance(data, int):
            data_bytes = bytearray([data])
        else:
            data_bytes = bytearray(data)

        if len(data_bytes) > 8:
            data_bytes = data_bytes[:8]

        dlc = len(data_bytes)

        while len(data_bytes) < 8:
            data_bytes.append(0)

        frame = struct.pack(
            can_frame_format,
            can_id,
            dlc,
            bytes(data_bytes),
        )

        s.send(frame)
        s.close()

        print(
            f"CAN Sent: ID 0x{can_id:x} "
            f"Data {list(data_bytes[:dlc])}"
        )

    except Exception as e:
        print(f"Error sending via SocketCAN: {e}")


def send_stop_command():

    throttle = 0
    steering = 0

    # First: enable/select drive command frame.
    send_can_native(ENABLE_DRIVE_CAN_ID, 1)
    sleep(0.02)

    # Then: send throttle and steering as zero.
    data = [
        throttle & 0xFF,
        (throttle >> 8) & 0xFF,
        steering & 0xFF,
        (steering >> 8) & 0xFF,
    ]

    send_can_native(DRIVE_COMMAND_CAN_ID, data)


# --- Arguments ---
if len(sys.argv) < 2:
    print("Usage:")
    print("  python3 /home/run.py --<directory>")
    print()
    print("Example:")
    print("  python3 /home/run.py --pipeline")
    print()
    print("With extra main.py flags:")
    print("  python3 /home/run.py --pipeline --virtual --no-display")
    sys.exit(1)


target_dir = sys.argv[1].lstrip("--")
main_script = f"/home/{target_dir}/main.py"

extra_args = sys.argv[2:]


print("=" * 60)
print("Starting pipeline")
print(f"Main script : {main_script}")

if extra_args:
    print(f"Extra args  : {' '.join(extra_args)}")

print("=" * 60)


# --- Start processes ---
joystick_process = subprocess.Popen(["/home/control"])

py_process = subprocess.Popen([
    "python3",
    main_script,
    "/home/models/yolo26n_seg_640.hef",
    "/home/models/yolo26n_v6.hef",
    *extra_args,
])


def shutdown(sig=None, frame=None):
    if hasattr(shutdown, "_done"):
        return

    shutdown._done = True

    print("\n[Shutdown] Sending CAN stop sequence...")

    # Repeat the sequence a few times to improve reliability.
    send_stop_command()
    sleep(0.05)
    send_stop_command()
    sleep(0.05)
    send_stop_command()

    sleep(0.2)

    print("Stopping processes...")

    if joystick_process.poll() is None:
        joystick_process.terminate()

    if py_process.poll() is None:
        py_process.terminate()

    try:
        py_process.wait(timeout=0.5)
        print("Pipeline closed normally.")
    except subprocess.TimeoutExpired:
        print("Pipeline stuck. Forcing KILL...")
        py_process.kill()

    if joystick_process.poll() is None:
        joystick_process.kill()

    print("Sequence complete. Exiting now.")

    os._exit(0)


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)


try:
    py_process.wait()
except KeyboardInterrupt:
    pass
finally:
    shutdown()

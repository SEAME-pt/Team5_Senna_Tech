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

    can_frame_format = "=IB3x8s"

    try:
        s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        s.bind((interface,))

        if isinstance(data, int):
            data_bytes = bytearray([data] + [0] * 7)
            dlc = 1
        else:
            data_bytes = bytearray(data)

            if len(data_bytes) > 8:
                data_bytes = data_bytes[:8]

            dlc = len(data_bytes)

            while len(data_bytes) < 8:
                data_bytes.append(0)

        frame = struct.pack(can_frame_format, can_id, dlc, bytes(data_bytes))

        s.send(frame)
        s.close()

        print(f"CAN Sent (Native): ID 0x{can_id:x} Data {list(data_bytes[:dlc])}")

    except Exception as e:
        print(f"Error sending via SocketCAN: {e}")


def send_stop_command():

    throttle = 0
    steering = 0

    send_can_native(ENABLE_DRIVE_CAN_ID, 1, CAN_INTERFACE)
    sleep(0.02)

    data = [
        throttle & 0xFF,
        (throttle >> 8) & 0xFF,
        steering & 0xFF,
        (steering >> 8) & 0xFF,
    ]

    send_can_native(DRIVE_COMMAND_CAN_ID, data, CAN_INTERFACE)


# --- Argumentos ---
if len(sys.argv) < 4:
    print("Usage:")
    print("  python3 /home/run_robotaxi.py --<directory> <pickup> <dropoff>")
    print()
    print("Example:")
    print("  python3 /home/run_robotaxi.py --pipeline_robotaxi 5,8 10,4")
    print()
    print("With extra main.py flags:")
    print("  python3 /home/run_robotaxi.py --robotaxi_yasmine 5,8 10,4 --virtual --no-display")
    sys.exit(1)


target_dir = sys.argv[1].lstrip("--")
main_script = f"/home/{target_dir}/main.py"

pickup = sys.argv[2]
dropoff = sys.argv[3]

extra_args = sys.argv[4:]


print("=" * 60)
print("Starting Robo Taxi pipeline")
print(f"Main script : {main_script}")
print(f"Pickup      : {pickup}")
print(f"Dropoff     : {dropoff}")

if extra_args:
    print(f"Extra args  : {' '.join(extra_args)}")

print("=" * 60)


joystick_process = subprocess.Popen(["/home/control"])

py_process = subprocess.Popen([
    "python3",
    main_script,
    "/home/models/yolo26n_seg_640.hef",
    "/home/models/yolo26n_v6.hef",
    pickup,
    dropoff,
    *extra_args,
])


def shutdown(sig=None, frame=None):
    if hasattr(shutdown, "_done"):
        return

    shutdown._done = True

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
        print("Hailo Pipeline exited normally.")
    except subprocess.TimeoutExpired:
        print("Hailo stuck on 'Freeing pipeline'. Forcing KILL...")
        py_process.kill()

    if joystick_process.poll() is None:
        joystick_process.kill()

    print("Sequence complete. Exiting now")

    os._exit(0)


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)


try:
    py_process.wait()
except KeyboardInterrupt:
    pass
finally:
    shutdown()

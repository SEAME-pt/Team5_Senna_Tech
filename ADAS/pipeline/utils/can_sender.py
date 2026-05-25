import can
import struct

class CanSender:
    def __init__(self, channel="can0", bitrate=500000):
        self.bus = can.interface.Bus(
            channel=channel,
            interface="socketcan"
        )

    def send_int16(self, can_id: int, value: int):
        # clamp and pack as int16 little-endian
        value = max(-32768, min(32767, value))

        data = struct.pack("<h", value)

        msg = can.Message(
            arbitration_id=can_id,
            data=data,
            dlc=2,
            is_extended_id=False
        )

        try:
            self.bus.send(msg)
        except can.CanError:
            print("CAN send failed")

    def send_can_percent(self, can_id: int, percent: float):
        # clamp -1.0 to 1.0
        percent = max(-1.0, min(1.0, percent))

        value = int(percent * 100)
        self.send_int16(can_id, value)

    def send_fsm_state(self, can_id: int, state_value: int):
        """ Sends the enumerated state of the FSM as an integer (1 byte) """
        # pack as unsigned char (1 byte, e.g. 0=FREE, 1=FOLLOW, 2=SLOW, 3=STOP, 4=EMERG)
        data = struct.pack("<B", state_value)
        msg = can.Message(
            arbitration_id=can_id,
            data=data,
            dlc=1,
            is_extended_id=False
        )

        try:
            self.bus.send(msg)
        except can.CanError:
            print("CAN send failed (FSM State)")

    # Not yet in use — waiting for PID to be moved to the MCU
    def send_cte(self, can_id: int, cte: float):
        """ Send the CTE multiplying by a factor to send as int16 """
        # multiply by 1000 to preserve 3 decimal places (e.g. 0.125 -> 125)
        # the MCU must divide by 1000.0
        value = int(cte * 1000)
        self.send_int16(can_id, value)

    def send_drive_command(self, can_id: int, throttle: int, steering: float):
        """
        Sends throttle + steering in a single CAN frame.

        Payload:
        bytes 0-1 -> throttle (int16)
        bytes 2-3 -> steering (int16 scaled by 100)
        """

        # clamp trottle and steering
        throttle    = max(-32768, min(32767, throttle))
        steering    = max(-1.0, min(1.0, steering))
        # Preserve 2 decimal places
        steering_i16 = int(steering * 100)
        # pack both int16 values
        data = struct.pack("<hh", throttle, steering_i16)
        msg  = can.Message(arbitration_id=can_id, data=data, dlc=4, is_extended_id=False)
        try:
            self.bus.send(msg)
        except can.CanError:
            print("CAN send failed (drive command)")

    def close(self):
        if self.bus:
            self.bus.shutdown()

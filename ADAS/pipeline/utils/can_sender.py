import can
import struct

class CanSender:
    def __init__(self, channel="can0", bitrate=500000):
        self.bus = can.interface.Bus(
            channel=channel,
            interface="socketcan"
        )

    def send_int16(self, can_id: int, value: int):
        # little-endian
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
        # clamp -1.0 a 1.0
        percent = max(-1.0, min(1.0, percent))

        value = int(percent * 100)
        self.send_int16(can_id, value)

    def send_fsm_state(self, can_id: int, state_value: int):
        """ Envia o estado enumerado da FSM como um inteiro (1 byte) """
        # Empacota um unsigned char (1 byte, ex: 0=FREE, 1=FOLLOW, 2=SLOW, 3=STOP, 4=EMERG)
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

    def send_drive_command(self, can_id: int, throttle: int, steering: float):
        """
        Sends throttle + steering in a single CAN frame.

        Payload:
        bytes 0-1 -> throttle (int16)
        bytes 2-3 -> steering (int16 scaled by 100)
        """

        # clamp throttle & steering
        throttle = max(-32768, min(32767, throttle))
        steering = max(-1.0, min(1.0, steering))

        # preserve 2 decimal places
        steering_i16 = int(steering * 100)

        # pack both int16 values
        data = struct.pack("<hh", throttle, steering_i16)

        msg = can.Message(
            arbitration_id=can_id,
            data=data,
            dlc=4,
            is_extended_id=False
        )
        try:
            self.bus.send(msg)
    
        except can.CanError:
            print("CAN send failed (drive command)")

    def close(self):
        if self.bus:
            self.bus.shutdown()


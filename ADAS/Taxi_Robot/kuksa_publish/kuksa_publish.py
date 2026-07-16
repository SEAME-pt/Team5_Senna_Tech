from kuksa.val.v1 import val_pb2 as val_v1
from kuksa.val.v1 import types_pb2 as types_v1
from kuksa.val.v1 import val_pb2_grpc as val_grpc_v1
import grpc
from object.perception_objects import Detection, ClassID

class KuksaClient:
    def __init__(self, address="localhost:55555"):
        self.channel = grpc.insecure_channel(address)
        self.stub = val_grpc_v1.VALStub(self.channel)

    # ---------------------------
    # Speed Signal Mappins
    # ---------------------------
    def detect_speed_signal(self, class_id):
        if class_id == ClassID.SIGN_50:
            return 11
        elif class_id == ClassID.SIGN_80:
            return 12
        return 10

    # ---------------------------
    # Traffic Signal Mappins
    # ---------------------------
    def detect_traffic_signal(self, class_id):
        mapping = {
            ClassID.CROSSWALK_SIGN: 3,
            ClassID.STOP_SIGN:      1,
            ClassID.YIELD_SIGN:     4,
            ClassID.DANGER_SIGN:    2,
            ClassID.LIGHT_GREEN:    7,
            ClassID.LIGHT_RED:      5,
            ClassID.LIGHT_YELLOW:   6
        }
        return mapping.get(class_id, 0)

    # ---------------------------
    # Select closer detection
    # ---------------------------
    _SPEED_CLASSES   = {ClassID.SIGN_50, ClassID.SIGN_80}
    _TRAFFIC_CLASSES = {ClassID.CROSSWALK_SIGN, ClassID.STOP_SIGN, ClassID.YIELD_SIGN,
                        ClassID.DANGER_SIGN, ClassID.LIGHT_GREEN, ClassID.LIGHT_RED, ClassID.LIGHT_YELLOW}

    def _select_signals(self, detections):
        current_speed_signal   = Detection(ClassID.LIGHT_YELLOW, False, 0.0)
        current_traffic_signal = Detection(ClassID.LIGHT_YELLOW, False, 0.0)

        for d in detections:
            if d.class_id in self._SPEED_CLASSES:
                if d.relative_area > current_speed_signal.relative_area:
                    current_speed_signal = d

            elif d.class_id in self._TRAFFIC_CLASSES:
                if d.relative_area > current_traffic_signal.relative_area:
                    current_traffic_signal = d

        return current_speed_signal, current_traffic_signal

    # ---------------------------
    # Send correct signal to Kuksa
    # ---------------------------
    def send(self, detections, robotaxi_state=None):
        speed_signal, traffic_signal = self._select_signals(detections)

        speed = self.detect_speed_signal(speed_signal.class_id)
        traffic = self.detect_traffic_signal(traffic_signal.class_id)

        updates = [
            val_v1.EntryUpdate(
                entry=types_v1.DataEntry(
                    path="Vehicle.ADAS.SpeedLimitSign",
                    value=types_v1.Datapoint(uint32=speed)
                ),
                fields=[types_v1.Field.Value("FIELD_VALUE")]
            ),
            val_v1.EntryUpdate(
                entry=types_v1.DataEntry(
                    path="Vehicle.ADAS.TrafficSign",
                    value=types_v1.Datapoint(uint32=traffic)
                ),
                fields=[types_v1.Field.Value("FIELD_VALUE")]
            )
        ]

        if robotaxi_state is not None:
            updates.append(
                val_v1.EntryUpdate(
                    entry=types_v1.DataEntry(
                        path="Vehicle.ADAS.Robotaxi.State",
                        value=types_v1.Datapoint(uint32=int(robotaxi_state))
                    ),
                    fields=[types_v1.Field.Value("FIELD_VALUE")]
                )
            )

        request = val_v1.SetRequest(updates=updates)

        response = self.stub.Set(request)

        """ if response.error.code != 0:
            print(f"[KUKSA] Erro: {response.error.message}")
        else:
            print(f"[KUKSA] Speed={speed} Traffic={traffic}") """

    def close(self):
        self.channel.close()

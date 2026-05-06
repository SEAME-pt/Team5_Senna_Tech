from kuksa.val.v1 import val_pb2 as val_v1
from kuksa.val.v1 import types_pb2 as types_v1
from kuksa.val.v1 import val_pb2_grpc as val_grpc_v1
import grpc
from object.perception_objects import Detection

class KuksaClient:
    def __init__(self, address="localhost:55555"):
        self.channel = grpc.insecure_channel(address)
        self.stub = val_grpc_v1.VALStub(self.channel)

    # ---------------------------
    # Speed Signal Mappins
    # ---------------------------
    def detect_speed_signal(self, id):
        if id == 0:
            return 11
        elif id == 1:
            return 12
        return 10

    # ---------------------------
    # Traffic Signal Mappins
    # ---------------------------
    def detect_traffic_signal(self, id):
        mapping = {
            3: 3,
            4: 1,
            5: 4,
            7: 2,
            9: 7,
            11: 5,
            12: 6
        }
        return mapping.get(id, 0)

    # ---------------------------
    # Select closer detection
    # ---------------------------
    def _select_signals(self, detections):
        current_speed_signal = Detection(13, False, 0.0)
        current_traffic_signal = Detection(13, False, 0.0)

        for d in detections:
            if d.class_id in (0, 1):
                if d.relative_area > current_speed_signal.relative_area:
                    current_speed_signal = d

            elif 2 < d.class_id < 13:
                if d.relative_area > current_traffic_signal.relative_area:
                    current_traffic_signal = d

        return current_speed_signal, current_traffic_signal

    # ---------------------------
    # Send correct signal to Kuksa
    # ---------------------------
    def send(self, detections):
        speed_signal, traffic_signal = self._select_signals(detections)

        speed = self.detect_speed_signal(speed_signal.class_id)
        traffic = self.detect_traffic_signal(traffic_signal.class_id)

        request = val_v1.SetRequest(
            updates=[
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
        )

        #response = self.stub.Set(request)

        #if response.error.code != 0:
            #print(f"[KUKSA] Erro: {response.error.message}")
       # else:
            #print(f"[KUKSA] Speed={speed} Traffic={traffic}")

    def close(self):
        self.channel.close()

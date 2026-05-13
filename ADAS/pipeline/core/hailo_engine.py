import cv2
import numpy as np
from hailo_platform import (
    ConfigureParams, HEF, HailoStreamInterface,
    InferVStreams, InputVStreamParams, OutputVStreamParams,
    FormatType, VDevice
)

class HailoEngine:
    def __init__(self, hef_path: str, target):
        self.hef_path = hef_path
        self.hef = HEF(hef_path)

        input_info = self.hef.get_input_vstream_infos()[0]
        self.net_size = 640
        self.input_name = input_info.name

        self.target = target
        self.pipeline = None
        self._ng = None

    def preprocess(self, img_bgr):
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img_rgb, (self.net_size, self.net_size))
        return np.expand_dims(img_resized, axis=0).astype(np.uint8)

    def __enter__(self):

        cfg = ConfigureParams.create_from_hef(
            self.hef,
            interface=HailoStreamInterface.PCIe
        )

        self._ng = self.target.configure(self.hef, cfg)[0]

        in_p = InputVStreamParams.make(self._ng)
        out_p = OutputVStreamParams.make(
            self._ng,
            format_type=FormatType.FLOAT32
        )

        self.pipeline = InferVStreams(self._ng, in_p, out_p)
        self.pipeline.__enter__()

        self.input_name = list(in_p.keys())[0]

        return self

    def infer(self, img_bgr):
        input_np = self.preprocess(img_bgr)

        # ativa só durante inferência
        with self._ng.activate(self._ng.create_params()):
            outputs = self.pipeline.infer({self.input_name: input_np})

        return outputs

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.pipeline:
            self.pipeline.__exit__(exc_type, exc_val, exc_tb)
import cv2
import logging
import numpy as np
from hailo_platform import (
    ConfigureParams,
    HEF,
    HailoStreamInterface,
    InferVStreams,
    InputVStreamParams,
    OutputVStreamParams,
    FormatType,
    VDevice,
)


class HailoEngine:
    def __init__(self, hef_path: str, target, debug: bool = False):
        self.hef_path = hef_path
        self.hef = HEF(hef_path)

        input_info = self.hef.get_input_vstream_infos()[0]
        self.net_size = 640
        self.input_name = input_info.name

        self.target = target
        self.pipeline = None
        self._ng = None
        self.debug = debug
        self.logger = logging.getLogger(__name__)

    def preprocess(self, img_rgb):
        img_resized = cv2.resize(img_rgb, (self.net_size, self.net_size))
        input_np = np.expand_dims(img_resized, axis=0).astype(np.uint8)
        if self.debug:
            self.logger.debug(
                "[INFERENCE] preprocess rgb=%s resized=%s batch=%s dtype=%s",
                img_rgb.shape,
                img_resized.shape,
                input_np.shape,
                input_np.dtype,
            )
        return input_np

    def __enter__(self):
        if self.debug:
            self.logger.debug("[INFERENCE] loading HEF: %s", self.hef_path)
        cfg = ConfigureParams.create_from_hef(
            self.hef,
            interface=HailoStreamInterface.PCIe,
        )

        self._ng = self.target.configure(self.hef, cfg)[0]

        in_p = InputVStreamParams.make(self._ng)
        out_p = OutputVStreamParams.make(
            self._ng,
            format_type=FormatType.FLOAT32,
        )

        self.pipeline = InferVStreams(self._ng, in_p, out_p)
        self.pipeline.__enter__()

        self.input_name = list(in_p.keys())[0]
        if self.debug:
            self.logger.debug(
                "[INFERENCE] engine ready input_name=%s net_size=%s",
                self.input_name,
                self.net_size,
            )
        return self

    def infer(self, img_rgb):
        input_np = self.preprocess(img_rgb)

        with self._ng.activate(self._ng.create_params()):
            outputs = self.pipeline.infer({self.input_name: input_np})

        if self.debug:
            output_shapes = {name: value.shape for name, value in outputs.items()}
            self.logger.debug("[INFERENCE] output keys=%s", list(outputs.keys()))
            self.logger.debug("[INFERENCE] output shapes=%s", output_shapes)
        return outputs

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.debug:
            self.logger.debug("[INFERENCE] closing engine: %s", self.hef_path)
        if self.pipeline:
            self.pipeline.__exit__(exc_type, exc_val, exc_tb)

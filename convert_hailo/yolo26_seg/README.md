# yolo26_seg — Conversion and Inference on Hailo-8

Full pipeline for converting and running **yolo26n-seg** and **yolo26s-seg** models
on the Hailo-8 (26 TOPS) via Raspberry Pi 5, applied to the LKA (Lane Keeping Assist) system.

---

## Structure

```
yolo26_seg/
├── scripts/
│   ├── test_yolo26_hailo.py        # v1 — initial prototype
│   ├── test_yolo26_hailo2.py       # v2 — full overlay
│   ├── test_yolo26_hailo3.py       # v3 — current LKA (use this one)
│   └── conversion/                 # ONNX→HEF conversion scripts
│       ├── pipeline.sh             # full automated pipeline
│       ├── cut_onnx.sh             # generic ONNX cut
│       ├── cut_onnx_nano.sh        # 3 outputs (nano format)
│       ├── cut_onnx_small.sh       # 10 outputs (small format)
│       ├── translate.sh            # ONNX → HAR (inside Docker)
│       ├── quantize.sh             # INT8 quantization (inside Docker)
│       ├── compile_hef.sh          # HAR → HEF BYOM (inside Docker)
│       └── recover_har.sh          # post-QFT recovery
└── docs/
    ├── 01_overview.md
    ├── 02_onnx_export.md
    ├── 03_translation_parsing.md
    ├── 04_quantization_calibration.md
    ├── 05_hef_compilation.md
    ├── 06_complete_flow_reference.md
    ├── 07_yolo26_seg_study.md
    ├── 08_nano_rpi5_test.md        # setup and execution on RPi5
    ├── 09_lka_overlay.md           # visual overlay + LKA/PID data
    ├── 10_benchmark_hailo8.md      # hailortcli benchmark results
    ├── 11_pcie_desc_page_size.md   # AGL PCIe DMA fix
    ├── NANO_TEST_GUIDE.txt         # quick test guide
    └── Journey.md                  # full technical journey log
```

---

## Local configuration

Copy and fill in the `.env.hailo` file at the `convert_hailo/` root:

```bash
cp ../../../.env.hailo.example ../../../.env.hailo
# edit with your local paths and RPi5 address
```

The `pipeline.sh` script loads this file automatically.

---

## Current script: test_yolo26_hailo3.py

### Execution

```bash
# Remote (view from host via ffplay):
ssh <rpi5-host> \
  "python3 test_yolo26_hailo3.py camera yolo26n_seg_640.hef --remote" \
  | ffplay -f mjpeg -i pipe:0

# Local on RPi5:
python3 test_yolo26_hailo3.py camera yolo26n_seg_640.hef

# With NPU monitor:
HAILO_MONITOR=1 python3 test_yolo26_hailo3.py camera yolo26n_seg_640.hef --remote
```

### Transfer to RPi5

```bash
scp yolo26_seg/scripts/test_yolo26_hailo3.py <rpi5-host>:~/
```

---

## Models available on RPi5

| Model | HEF | Size | max FPS (hw) | HW Latency |
|---|---|---|---|---|
| yolo26n_seg_640 | `~/yolo26n_seg_640.hef` | 9.1 MB | 68.72 FPS | 13.45 ms |
| yolo26s_seg_640 | `~/yolo26s_seg_640.hef` | — | 33.24 FPS | 28.50 ms |

Hardware: Hailo-8 (26 TOPS), compiled on 06/04/2026.

---

## Conversion pipeline

See `docs/06_complete_flow_reference.md` for the full step-by-step
(ONNX → HAR → HEF via Docker Hailo AI SW Suite).

For yolov8-seg conversion, see `../convert_flow/`.

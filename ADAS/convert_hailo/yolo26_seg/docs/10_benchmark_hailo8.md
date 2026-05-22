# Hailo-8 Benchmark — yolo26n/s-seg

Results measured with `hailortcli benchmark` on RPi5 on 07/04/2026.

Hardware: **Hailo-8 (26 TOPS)** + Raspberry Pi 5.

---

## Results

### yolo26n_seg_640.hef

```
hailortcli benchmark ~/yolo26n_seg_640.hef
```

| Metric | Value |
|---|---|
| FPS hw_only | **68.72 FPS** |
| FPS streaming | 68.71 FPS |
| HW Latency | **13.45 ms** |
| HEF size | 9.1 MB |
| Contexts | 3 |

### yolo26s_seg_640.hef

```
hailortcli benchmark ~/yolo26s_seg_640.hef
```

| Metric | Value |
|---|---|
| FPS hw_only | **33.24 FPS** |
| FPS streaming | 33.24 FPS |
| HW Latency | **28.50 ms** |
| Contexts | 4 |

---

## Runtime Usage

### Real-time monitoring

```bash
# Terminal 1 — run inference with monitoring enabled
HAILO_MONITOR=1 python3 test_yolo26_hailo3.py camera yolo26n_seg_640.hef --remote

# Terminal 2 — open the monitor
hailortcli monitor
```

### NPU utilization calculation in overlay

```
NPU% = (current_fps / max_hw_fps) × 100 × 0.95
```

The `0.95` factor corrects the observed difference between the calculation and `hailortcli monitor`.

| Model | max_hw_fps | Example (25 FPS) |
|---|---|---|
| yolo26n_seg_640 | 68.72 | ~35% NPU |
| yolo26s_seg_640 | 33.24 | ~71% NPU |

---

## parse-hef

```bash
hailortcli parse-hef ~/yolo26n_seg_640.hef
```

```
Architecture HEF was compiled for: HAILO8
Network group name: yolo26n_seg_640, Multi Context - Number of contexts: 3
    Network name: yolo26n_seg_640/yolo26n_seg_640
        VStream infos:
            Input  yolo26n_seg_640/input_layer1 UINT8, NHWC(640x640x3)
            Output yolo26n_seg_640/ew_mult1 UINT8, NHWC(1x8400x4)
            Output yolo26n_seg_640/activation3 UINT8, NHWC(1x8400x1)
            Output yolo26n_seg_640/concat22 UINT8, FCR(1x8400x32)
            Output yolo26n_seg_640/conv109 UINT8, FCR(160x160x32)
```

**Note:** `parse-hef` does not expose MACs/GOPs. The number of operations is not
available via CLI without using the Hailo DFC profiler.

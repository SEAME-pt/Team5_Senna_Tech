# LKA Overlay — Visualization and Output Data

Full visualization pipeline for the LKA system with yolo26n/s-seg on Hailo-8.

---

## Visual Overlay (draw_text_overlay)

The `test_yolo26_hailo3.py` script draws two information blocks on the frame:

### Top-right
```
yolo26n_seg_640
```
Name of the loaded HEF model (derived from filename).

### Footer — Line 1 (latencies)
```
Hailo: 13.5ms  FPS: 25.0  NPU: 36%  Post: 8.1ms  Temp: 67C
```

| Field | Source | Description |
|---|---|---|
| `Hailo: Xms` | `inf_ms` | Inference latency on the Hailo-8 chip |
| `FPS: X` | `fps` | Frames processed per second (average since start) |
| `NPU: X%` | `fps / max_hw_fps × 100 × 0.95` | NPU utilization (see below) |
| `Post: Xms` | `cpu_ms` | Python post-processing time (mask→BEV→polyfit) |
| `Temp: XC` | `/sys/class/thermal/thermal_zone0/temp` | RPi5 temperature |

### Footer — Line 2 (CPU)
```
CPU: 74% used  free: 26%
```

| Field | Source |
|---|---|
| `used` | `cpu_pct_user + cpu_pct_sys` via `/proc/stat` |
| `free` | `cpu_pct_idle` via `/proc/stat` |

### Geometric Overlay (draw_lane_overlay)
- Left lane: blue line
- Right lane: red line
- Area between lanes: semi-transparent green fill
- Center line: yellow (BEV + unwarped)
- CTE bar: frame center, yellow circular indicator

---

## NPU Utilization Calculation

Utilization is calculated based on the `hailortcli benchmark`:

```
NPU% = (current_fps / max_hw_fps) × 100 × 0.95
```

The `0.95` factor is an empirical correction — `hailortcli monitor` consistently showed
~5% less than the value calculated without the correction.

### Reference values (measured 07/04/2026)

| Model | hw_only FPS | HW Latency |
|---|---|---|
| `yolo26n_seg_640` | 68.72 FPS | 13.45 ms |
| `yolo26s_seg_640` | 33.24 FPS | 28.50 ms |

Hardware: Hailo-8 (26 TOPS) + Raspberry Pi 5.

---

## LaneFitResult — Data Available for PID/MPC

The `LaneFitResult` object returned each frame contains:

| Field | Type | Description | Available |
|---|---|---|---|
| `cte_meters` | float | Lateral error in meters (PID input) | ✅ |
| `cte_pixels` | float | Lateral error in pixels | ✅ |
| `curvature_meters` | float | Curvature radius in meters | ✅ |
| `left_found` | bool | Left lane detected | ✅ |
| `right_found` | bool | Right lane detected | ✅ |
| `left_fit` | ndarray | Left polynomial coefficients | ✅ |
| `right_fit` | ndarray | Right polynomial coefficients | ✅ |
| `heading_error` | float | Vehicle angle relative to lane | ❌ (future) |

### What is missing for full PID/MPC

| Field | Source | Notes |
|---|---|---|
| `heading_error` | derivable from `left_fit`/`right_fit` | to implement |
| `timestamp` | `time.time()` | to add to LaneFitResult |
| `lane_width` | internal `_ppm_x` | not exposed yet |
| Speed | CAN bus / odometry | external to script |

---

## STM32 Architecture (future)

```
RPi5 + Hailo-8                STM32
─────────────────             ─────────────────
cte_meters       ──CAN 0x200──▶ PID loop @ 1kHz
curvature_meters              ▶ PWM servo/motor
left_found                    ▶ Watchdog (~200ms)
right_found
counter (rolling)
```

### Proposed CAN frame (8 bytes, ID 0x200)

| Bytes | Field | Encoding |
|---|---|---|
| 0–1 | CTE | int16, mm |
| 2–3 | Curvature | int16, cm |
| 4 | Flags | bit0=left, bit1=right, bit2=valid |
| 5 | Counter | 0–255 rolling |
| 6–7 | Reserved | — |

All required fields are already available in the current script.

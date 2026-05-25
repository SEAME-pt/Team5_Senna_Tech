# Study: YOLO26s-seg on Hailo-8

## Model data (confirmed via export)

| Property | Value |
|-------------|-------|
| Model | YOLO26s-seg |
| Framework | Ultralytics 8.4.24 |
| PyTorch | 2.10.0+cu128 |
| Layers (fused) | 139 |
| Parameters | 10,365,727 |
| GFLOPs | 34.1 |
| ONNX size | 39.9 MB |
| Input shape | (1, 3, 640, 640) BCHW |
| Output shapes | (1, 300, 38) + (1, 32, 160, 160) |
| Opset | 17 (required for 640x640 — fixes attention Reshape) |
| Export time | 4.4s |

## Output architecture (NMS-Free)

YOLO26 differs significantly from YOLOv8 in its output:

### YOLOv8-seg (legacy)
- 3 detection tensors (scales 8, 16, 32 strides)
- 1 prototype tensor (160x160x32)
- Requires NMS in post-processing (software or hardware)

### YOLO26s-seg (new)
- **1 detection tensor**: (1, 300, 38) — 300 fixed proposals, already filtered
  - 38 = 4 (bbox) + 1 (score) + 1 (class) + 32 (mask coefficients)
- **1 prototype tensor**: (1, 32, 160, 160) — base masks
- **NMS-free**: the model performs selection internally (end-to-end)
- **No NMS required in post-processing**

## Implications for the Hailo pipeline

### Advantages
- Much simpler post-processing (no NMS)
- Fewer CPU operations on the RPi5 after inference
- Deterministic output (always 300 proposals)
- Compatible with Hailo raw output mode

### Required changes in TSHailo.py
- The `YoloV8SegPost` class needs to be adapted or replaced
- No longer necessary to merge 3 detection scales
- The proto × coefficients multiplication remains the same
- Parsing the 300x38 is more direct than the multi-scale format

### Compilation considerations (BYOM)
- Model larger than YOLOv8n-seg (39.9MB vs 13.3MB ONNX)
- May require more contexts in Hailo-8 partitioning
- `onnxsim` is recommended before parsing
- Verify ONNX input name (may not be "images")

## Size comparison

| Model | Params | GFLOPs | ONNX size |
|--------|--------|--------|-----------|
| YOLOv8n-seg | ~3.4M | ~12.0 | 13.3 MB |
| YOLO26s-seg | ~10.4M | ~34.1 | 39.9 MB |

YOLO26s-seg is ~3x larger than YOLOv8n-seg. Evaluate whether the Hailo-8
can accommodate the full model or if the nano variant is needed
(if available).

## Docker container environment (Hailo DFC)

When importing `hailo_sdk_client` inside the container, the DFC performed the system check:

| Component | Required | Found | Status |
|------------|-----------|------------|--------|
| OS | Ubuntu | Ubuntu 22.04 | OK |
| python3-tk | sim | sim | OK |
| graphviz | sim | sim | OK |
| python3.10-dev | sim | sim | OK |
| RAM | 16GB (min) / 32GB (rec) | 39GB | OK |
| CPU-Arch | x86_64 | x86_64 | OK |
| CPU-flag avx | sim | sim | OK |
| GPU Driver | 560 (rec) | **580** | OK |
| CUDA | **12.5 (rec)** | **11.8** | Warning |
| CUDNN | **9 (rec)** | **nao detectado** | Warning |

### Important notes

- **GPU was automatically detected**: `[info] Selected GPU 0`
- **CUDA 11.8 vs 12.5**: warning only, not blocking. CUDA 11.8 comes from the Docker image
  (hailo8_ai_sw_suite_2025-10), while the host has CUDA 13.0 with driver 580
- **CUDNN not detected**: warning only. May impact quantization performance
  but does not block compilation
- All "Required" items passed. Warnings are "Recommended"
- ONNX input name confirmed: `images`

## ONNX simplification (onnxsim)

```
Original: 39.9 MiB  ->  Simplificado: 39.8 MiB
```

- Removed 1 redundant `Constant` operation
- Model was already well optimized by the Ultralytics export
- Warning about `Tile` and `ConstantOfShape` ops (use `--no-large-tensor` if the
  simplified model becomes much larger than the original)

## Tile node analysis (translation blocker)

### Problem

`ClientRunner.translate_onnx_model()` fails because the ONNX contains 3 `Tile`
operations that the Hailo DFC does not support.

### Tile node locations

All 3 `Tile` nodes are in `/model.23/` (detection head), specifically
in the **end-to-end post-processing** logic (top-k selection):

| Node | Inputs | Output |
|----|--------|--------|
| `/model.23/Tile` | `Expand_output_0`, `ConstantOfShape_output_0` | `Tile_output_0` |
| `/model.23/Tile_1` | `Expand_1_output_0`, `onnx::Tile_803` | `Tile_1_output_0` |
| `/model.23/Tile_2` | `Expand_1_output_0`, `onnx::Tile_809` | `Tile_2_output_0` |

The Tiles build anchor grids for top-k selection that filters the 300 best
detections. After the Tiles, `Gather` and `GatherElements` follow until `output0` is produced.

### Graph structure in model.23

```
Backbone + Neck
    |
    v
Detection heads (one2one_cv2.*, cv3.*, cv4.*)
    |                                    |
    v                                    v
Reshape (x9)                        Proto branch
    |                                    |
    v                                    v
Concat (bbox) ----+                 output1 (1,32,160,160)  <-- OK, sem Tiles
Concat_1 (cls) ---+
Concat_2 (mask) --+
                  |
                  v
        Slice, Sub, Add, Sigmoid
                  |
                  v
            Concat_4  <-- CUT POINT (raw detections, all scales)
                  |
                  v
        Tile (x3), Gather, GatherElements  <-- BLOCKER (Hailo does not support Tile)
                  |
                  v
            output0 (1,300,38)
```

### Conclusion

It is not possible to compile the model with integrated end-to-end post-processing.
This is **expected behavior** in the Hailo ecosystem — even officially supported models
(YOLOv8, YOLOv5) run post-processing on the CPU, not the chip.

### Solution: cut the ONNX before the Tile nodes

Cut the model at the `Concat_4` node to expose 2 outputs:

- **`Concat_4_output_0`** — raw detections (bbox + scores + mask coefs, all scales)
- **`output1`** — mask prototypes (32x160x160)

The remaining post-processing (top-k selection of the 300 best detections) will run
on the RPi5 CPU. This operation is **lighter** than YOLOv8 NMS.

| | YOLOv8-seg | YOLO26s-seg |
|---|---|---|
| Chip output | 3 separate tensors + proto | concatenated tensor + proto |
| CPU post-proc | Full NMS (heavy) | Top-k selection (light) |

### Confirmed shapes (via onnx.shape_inference)

Internal tensors of `model.23`:

| Tensor | Shape | Contents |
|--------|-------|----------|
| `Concat_output_0` | `[1, 4, 8400]` | bbox (dist2bbox converted) |
| `Concat_1_output_0` | `[1, 1, 8400]` | scores (after sigmoid) |
| `Concat_2_output_0` | `[1, 32, 8400]` | mask coefficients |
| **`Concat_4_output_0`** | **`[1, 37, 8400]`** | **all concatenated (cut point)** |

Original model outputs:

| Tensor | Shape | Contents |
|--------|-------|----------|
| `output0` | `[1, 300, 38]` | top-300 detections (post top-k, contains Tiles) |
| `output1` | `[1, 32, 160, 160]` | mask prototypes |

Breakdown of `Concat_4` (37 channels):
- `[0:4]` = 4 bbox values (coordinates)
- `[4:5]` = 1 confidence score
- `[5:37]` = 32 mask coefficients

Breakdown of 8400 proposals (3 scales):
- 80x80 = 6400 (stride 8, small objects)
- 40x40 = 1600 (stride 16, medium objects)
- 20x20 = 400 (stride 32, large objects)

### Outputs after the cut

The cut ONNX will have 2 outputs:

| Output | Shape | Description |
|-------|-------|-----------|
| `Concat_4_output_0` | `[1, 37, 8400]` | raw detections (all scales) |
| `output1` | `[1, 32, 160, 160]` | mask prototypes (unchanged) |

### Conversion flow with cut

The cut is performed on the ONNX, before entering the Hailo pipeline:

```
best.pt
  |  (ultralytics export)
  v
best.onnx  (original, com Tiles — Hailo nao aceita)
  |  (script de corte: remove nos pos Concat_4)
  v
best_cut.onnx  (sem Tiles — Hailo aceita)
  |  (translate_onnx_model)
  v
yolo26s_seg.har
  |  (optimize / quantize)
  v
yolo26s_seg_quantized.har
  |  (compile)
  v
yolo26s_seg.hef  (roda no Hailo-8)
```

The removed post-processing (top-k selection) will be reimplemented on the RPi5 CPU.

## ONNX cut (result)

Script: `convert_flow/scripts/cut_onnx.sh` (runs inside the Docker container)

### Execution result

```
Nos antes:     433
Nos removidos: 15
Nos restantes: 418
Outputs: ['/model.23/Concat_4_output_0', 'output1']
Validacao OK
Original:  39.8 MB
Cortado:   39.8 MB
```

### Removed nodes (15)

Downstream of Tiles (14):
- `/model.23/Tile`, `/model.23/Tile_1`, `/model.23/Tile_2`
- `/model.23/TopK_1`
- `/model.23/GatherElements`, `/model.23/GatherElements_1`, `/model.23/GatherElements_2`
- `/model.23/Gather_3`
- `/model.23/Flatten`, `/model.23/Cast_2`, `/model.23/Mod`
- `/model.23/Unsqueeze_1`, `/model.23/Unsqueeze_2`
- `/model.23/Concat_7`

Orphan (1):
- `/model.23/Flatten_1` (only fed the Tiles)

### Notes

- Size practically unchanged (39.8 MB) — backbone weights remain,
  only the top-k logic was removed (weightless operations)
- `onnx.checker.check_model()` passed without errors
- Generated file: `best_cut.onnx`

## Translation / Parsing (result)

```
translate_onnx_model() com best_cut.onnx -> OK (sem erros)
save_har() -> yolo26s_seg.har (40.3 MB)
```

- The cut ONNX was accepted by the Hailo DFC without issues
- No unsupported operator warnings
- HAR generated at `/local/shared_with_docker/yolo26s_seg.har`

## Quantization (attempts)

### Attempt 1: optimize() with optimization_level=2

```
TypeError: ClientRunner.optimize() got an unexpected keyword argument 'optimization_level'
```

The `optimization_level` parameter was removed in suite 2025-10. The SDK
automatically uses level 2 by default.

### Attempt 2: optimize() without extra arguments

Basic calibration passed (Statistics Collector, 64 images), but
**Quantization-Aware Fine-Tuning (QFT)** failed with GPU OOM:

```
ResourceExhaustedError: GPU memory has been exhausted.
Detected at node yolo26s_seg_3/conv108_1/act_op_1/zeros_like_1
```

Available GPU: NVIDIA RTX 2000 Ada (8GB VRAM), clean (18MiB in use).
YOLO26s-seg (~10.4M params) is too large for QFT with default batch on 8GB.

Steps that passed before OOM:
| Step | Status |
|-------|--------|
| Mixed Precision | OK |
| Statistics Collector (calibration, 64 imgs) | OK |
| Fix zp_comp Encoding | OK |
| Matmul Equalization | OK |
| **QFT (fine-tuning, 1024 imgs)** | **OOM** |

### Attempt 3: batch_size via model script (.alls)

```
quantization_param(finetune, batch_size=2)
```

Failed: `batch_size` is not a valid key for `quantization_param`.
The SDK only accepts keys from `LayerPrecisionConfig` and `LayerTranslationConfig`.

### Attempt 4: batch_size as optimize() argument

```
TypeError: ClientRunner.optimize() got an unexpected keyword argument 'batch_size'
```

`optimize()` only accepts: `calib_data`, `data_type`, `work_dir`, `checkpoint`, `memento`.

### optimize() API (suite 2025-10)

```python
ClientRunner.optimize(
    self,
    calib_data,
    data_type=CalibrationDataType.auto,
    *,
    work_dir=None,
    checkpoint: SupportedStops = SupportedStops.NONE,
    memento: Optional[FlowCheckPoint] = None
)
```

### Batch size investigation via SDK source code

Located in `hailo_model_optimization.algorithms.finetune.qft`:

- `DEFAULT_BATCH_SIZE = 8` (default do QFT)
- O batch size real vem de `model_config.finetune.batch_size`
- Se for `None`, herda de `model_config.calibration.batch_size`
- Configurado em `QftRunner.finalize_global_cfg()`

```python
# qft.py linhas 576-579
if algo_config.batch_size is None:
    algo_config.batch_size = self._model_config.calibration.batch_size
if algo_config.learning_rate is None:
    algo_config.learning_rate = self.DEFAULT_LEARNING_RATE / DEFAULT_BATCH_SIZE * algo_config.batch_size
```

The `batch_size` is configurable via model script with the correct command:

```
post_quantization_optimization(finetune, batch_size=2)
```

**Not** via `quantization_param` (attempt 3 was wrong).
`FineTuneConfig` class in `hailo_model_optimization.acceleras.model_optimization_config.mo_config`:
- `batch_size`: default `None` (herda de `calibration.batch_size`)
- `val_batch_size`: default `128`
- `dataset_size`: default `DEFAULT_DATASET_SIZE`
- `epochs`: default `DEFAULT_EPOCHS`

### Attempt 5: quantize with 256 images (no GPU)

GPU had 6291MiB stuck from the previous session (dead process, memory not freed).
The SDK detected no usable GPU and ran with optimization level 0:

```
[warning] Reducing optimization level to 0 because there's less data than the recommended
          amount (1024), and there's no available GPU
[info] Bias Correction skipped
[info] Adaround skipped
[info] Quantization-Aware Fine-Tuning skipped
[info] Layer Noise Analysis skipped
[info] Model Optimization is done
HAR quantizado salvo: yolo26s_seg_quantized.har (204.3 MB)
```

HAR was generated but with minimum quality (level 0, no GPU, no QFT).

### Compilation attempt with HAR level 0

```
[error] Mapping Failed (allocation time: 13s)
No successful assignments: concat24 errors:
    Agent infeasible
[error] Failed to produce compiled graph
```

The model did not fit in the Hailo-8. Possible reasons:
1. Poorly quantized HAR (level 0 may generate sub-optimal layout configurations)
2. Model genuinely too large for the chip

Next test: compile with `compiler_optimization_level=max` and/or
redo quantization with clean GPU + level 2.

### Next step

1. ~~Verificar o shape de `Concat_4_output_0` via `onnx.shape_inference`~~ (feito)
2. ~~Cortar o ONNX no Concat_4~~ (feito — 15 nos removidos, validacao OK)
3. ~~Testar `translate_onnx_model()` com o ONNX cortado~~ (feito — HAR 40.3 MB)
## Quantization (final result)

Script: `convert_flow/scripts/quantize.sh` with model script:
```
post_quantization_optimization(finetune, policy=enabled, batch_size=2)
```

### Execution result

| Step | Status | Time |
|-------|--------|-------|
| Mixed Precision | OK | 0.74s |
| Statistics Collector (64 imgs) | OK | 36s |
| Fix zp_comp / Matmul Equalization | OK | ~1s |
| **Quantization-Aware Fine-Tuning** | **OK** | **12m52s** |
| Layer Noise Analysis | OK (warning GPU mem) | 4m19s |

```
QFT loss final: 0.7759
  concat24: 0.0196
  conv109:  0.3229
  conv95:   0.4334
```

Layer Noise Analysis completou com warning:
```
[warning] GPU memory has been exhausted. Layer Noise Analysis will not generate statistics.
```
Not blocking — the HAR was saved normally.

- Quantized HAR: `yolo26s_seg_quantized.har` (204.3 MB)
- Optimization level: 2 (with GPU, 1024 imgs)
- QFT batch size: 2 (reduced from 8 to fit in 8GB VRAM)

## Compilation (result)

The YOLO26s-seg model at 640x640 **did not fit in the Hailo-8** in any configuration:

| Attempt | Result |
|-----------|-----------|
| HAR level 0 (no GPU) | `concat24 Agent infeasible` |
| HAR level 2 (with GPU, QFT) | `No valid partition found` (6 attempts) |
| `compiler_optimization_level=max` | `No valid partition found` |

The bottleneck is two large simultaneous outputs:
- `output_layer1`: `[1, 1, 8400, 37]` — detections
- `output_layer2`: `[1, 160, 160, 32]` — proto masks

The combination exceeds the Hailo-8 SRAM.

## Resolution vs quality trade-off

### Analyzed options

| Option | Lane quality | CPU RPi5 | 30fps viable |
|-------|-----------------|----------|--------------|
| 640x640 + proto on chip | Maximum | Minimum | Blocked |
| 640x640 + proto on CPU | Maximum | ~100ms (unfeasible) | No |
| 416x416 retrained | Good | Minimum | Yes |
| 416x416 without retraining | Acceptable | Minimum | Yes |
| 320x320 | Low | Minimum | Yes |

### Why lane lines are resolution-sensitive

Road lane lines are thin, elongated objects — they depend on resolution for:
- Dashed lines (small segments)
- Lines in curves
- Distant lines
- The segmentation mask at 640 is already 160x160 (1/4). At 416 it would be 104x104.

### Decision taken

**Chosen option: 416x416 without retraining** as a starting point.

Rationale:
- Retraining requires time and resources
- 416x416 may be sufficient for wide lanes in good conditions
- Evaluate quality first before committing to retraining
- Requirement: 30fps (33ms/frame total)

### Future alternatives to explore

**A) Retrain YOLO26s-seg at 416x416**
- Better quality than running a 640 model at 416
- The model learns features at 416
- Procedure: `yolo train model=yolo26s-seg.pt imgsz=416 ...`

**B) Convert and test YOLO26n-seg (nano)**
- Smaller model, may fit the Hailo-8 at 640x640
- Maintain lane detection quality at maximum resolution
- **NOTE**: convert YOLO26n-seg to Hailo-8 following this same
  pipeline and compare efficiency (mAP, FPS, HEF size) with YOLO26s-seg at 416
- Procedure: same pipeline, replace `best.pt` with the trained nano model

## 416x416 pipeline (result)

### ONNX export at 416x416

```
Input shape:  (1, 3, 416, 416)
Output shapes: (1, 300, 38) + (1, 32, 104, 104)
Tamanho ONNX: 39.8 MB
```

### ONNX cut (cut_onnx.sh)

Same result as 640x640 — 15 nodes removed, validation OK.

### Translation (translate.sh yolo26s_seg_416 416)

```
HAR salvo: yolo26s_seg_416.har (40.2 MB)
```

### Quantization (quantize.sh yolo26s_seg_416 416)

| Metric | 640x640 | 416x416 |
|---------|---------|---------|
| total_distill_loss | 0.7759 | **0.7509** |
| QFT tempo | 12m52s | **7m31s** |
| SNR output_layer1 (detections) | n/a | **30.21 dB** |
| SNR output_layer2 (proto masks) | n/a | **11.02 dB** |
| Layer Noise Analysis | 50% (OOM) | **100% OK** |
| Quantized HAR | 204.3 MB | **208.0 MB** |

SNR output_layer2 (11.02 dB) is at the lower acceptable limit — may cause
noise in segmentation masks, especially for thin lines.

### Compilation (compile.sh yolo26s_seg_416)

```
Mapping:     Successful (12m59s)
Compilation: Successful (16s)
HEF:         yolo26s_seg_416.hef (20.2 MB)
Contexts:   4
```

Hailo-8 cluster utilization:

| Context | Clusters | Utilization |
|----------|----------|------------|
| 0 | 0-3 | ~65% |
| 1 | 4-7 | ~30% |
| 2 | 8-11 | ~45% |
| 3 | 12-13 | ~35% |

Well-balanced distribution. The 416x416 model fit comfortably in the chip
with 4 contexts.

### Complete 416x416 pipeline (final summary)

```
best.pt (treinado a 416x416)
  |  ultralytics export format=onnx imgsz=416
  v
best.onnx (39.8 MB)
  |  onnxsim
  v
best_simplified.onnx (39.7 MB)
  |  cut_onnx.sh (remove 15 nos Tile+downstream)
  v
best_cut.onnx (39.7 MB)
  |  translate.sh yolo26s_seg_416 416
  v
yolo26s_seg_416.har (40.2 MB)
  |  quantize.sh yolo26s_seg_416 416 (QFT batch=2, 1024 imgs)
  v
yolo26s_seg_416_quantized.har (208.0 MB)
  |  compile.sh yolo26s_seg_416
  v
yolo26s_seg_416.hef (20.2 MB) ✓
```

## Inference tests on RPi5 (results)

### Problem: scores zerados a 416x416 e 512x512

After transferring HEFs to the RPi5 and running inference with real camera frames,
scores for all detections were zero:

```
[Canal 4 - score UINT8]
  416x416: todos os valores = 66  (zero-point da quantizacao)
  512x512: todos os valores = 59  (zero-point da quantizacao)
```

Channels 0-3 (bbox) had real variance (values 13-242), confirming the
backbone is working. Only the classification head (score) and
mask coefficients (ch 5-36) were at zero-point.

### Diagnosis

The `best.pt` model was trained at **640x640**. When exporting at 416x416 or 512x512,
the detection head does not generalize — score logits are so negative
that sigmoid(logit) ≈ 0, and quantization rounds to zero-point.

| Resolution | Compilation | Scores | Decision |
|-----------|-----------|--------|---------|
| 640x640 | Failed (SRAM) | N/A | Infeasible with 2 outputs |
| 512x512 | OK (4 ctx) | Zero | Unusable |
| 416x416 | OK (4 ctx) | Zero | Unusable |

### Discarded resolution attempts

- **Capture camera directly at 416x416** (no resize): same result
- **Alternative post-processing**: impossible without valid scores
- **Remove proto branch and compile 640x640 detection-only**: loses segmentation

### Decision: remove proto and compile at 640x640 (detection-only)

Temporary approach while retraining is not available:
- Remove the proto branch (conv109) from the ONNX entirely
- Keep only the `concat24` output — raw detections at 640x640
- At 640x640 scores will be valid (training resolution)
- **The 32 mask coefficients (ch 5:37) are preserved in concat24**
- Current post-processing: bbox approximation for lane mask
- **Future post-processing**: when a retrained 416 model with proto is available,
  mask coefficients can be used with the proto reconstructed on CPU

### Information for future post-processing (with proto)

The `concat24` tensor at 640x640 will have shape `[1, 1, 8400, 37]`:
- `ch 0:4`  = bbox (cx, cy, w, h) in pixels relative to 640x640
- `ch 4`    = confidence score (post-sigmoid, range 0-1)
- `ch 5:37` = 32 mask coefficients

To reconstruct the mask when the proto is available:
```python
# expected proto shape: (32, 160, 160) at 640x640
mask = sigmoid(coeffs @ proto.reshape(32, -1)).reshape(160, 160)
mask = cv2.resize(mask, (orig_w, orig_h))
binary = (mask > 0.5).astype(np.uint8) * 255
```

The proto can come from:
- Model retrained at 416x416 (proto would be 104x104)
- YOLO26n-seg compiled separately running on CPU

### Next step

1. ~~Verificar shapes via onnx.shape_inference~~ (feito)
2. ~~Cortar ONNX no Concat_4~~ (feito — 15 nos removidos)
3. ~~Translate → Quantize → Compile a 416x416~~ (feito — HEF 20.2 MB)
4. ~~Compile a 512x512~~ (feito — HEF 20.5 MB)
5. ~~Testar inferencia na RPi5~~ (feito — scores zerados a 416 e 512)
6. Create `cut_onnx_noProto.sh` — removes Tiles + full proto branch
7. Export ONNX at 640x640 → cut → translate → quantize → compile (detection-only)
8. Test inference at 640x640 — confirm non-zero scores
9. Implement bbox-based post-processing in `test_yolo26_hailo.py`
10. Evaluate lane detection quality with bbox
11. Future: retrain at 416x416 to recover segmentation with proto

## Changelog

- March 31, 2026: Initial export and tests on machine team5@seame-5.
- March 31, 2026: Tile node analysis and cut strategy definition.
- March 31, 2026: Shapes confirmed via shape_inference. Cut point defined at Concat_4 [1,37,8400].
- March 31, 2026: ONNX cut executed successfully. 15 nodes removed, validation OK.
- March 31, 2026: translate_onnx_model() passed successfully. HAR generated (40.3 MB).
- March 31, 2026: Quantization level 0 (no GPU) generated HAR 204.3 MB. Compilation failed (model does not fit in chip).
- March 31, 2026: Found correct syntax for QFT batch size: post_quantization_optimization(finetune, policy=enabled, batch_size=2).
- March 31, 2026: Level 2 quantization with QFT completed. HAR 204.3 MB generated.
- March 31, 2026: Compilation failed in all attempts (640x640 too large). Decision: try 416x416 without retraining.
- March 31, 2026: Complete 416x416 pipeline up to quantization. HAR 208.0 MB, loss 0.7509, SNR 30.21/11.02 dB.
- March 31, 2026: HEF compilation successful. yolo26s_seg_416.hef (20.2 MB), 4 contexts, 12m59s mapping + 16s kernel compilation.
- April 1, 2026: RPi5 tests — zero scores at 416x416 and 512x512. Cause: model trained at 640, does not generalize to smaller resolutions without retraining.
- April 1, 2026: Decision: remove proto branch from ONNX and compile at 640x640 (detection-only). Mask coefficients preserved for future use with proto.
- April 1, 2026: cut_onnx_noProto.sh executed — 38 nodes removed (Tiles + proto branch + 1 orphan). Translate at 640x640 failed: Reshape /model.10/m/m.0/attn/Reshape {1,512,20,20}→{1,4,128,256} incompatible with Hailo DFC.
- April 1, 2026: Model fine-tuned at 416x416 — 5 epochs, lr0=0.001, dataset 698k imgs. mAP50=0.964, mAP50-95=0.753. Exported with opset=12.
- April 1, 2026: Complete fine-tuned 416x416 pipeline: translate OK, quantization OK (SNR 34.13/11.55 dB), compilation OK — yolo26s_seg_416.hef (21.1 MB), 4 contexts, proto included.
- April 1, 2026: RPi5 tests with fine-tuned HEF — ch4 (score) still zero (zero-point=55). 5-epoch fine-tune insufficient to recalibrate scores at 416x416.
- April 1, 2026: Critical discovery: exporting with opset=17 fixes attention mechanism shapes. With opset=12, /model.10/m/m.0/attn/Reshape has incompatible shapes {1,512,20,20}→{1,4,128,256}. With opset=17, onnxslim corrects to {1,512,13,13}→{1,4,128,169} (element counts match: 86528=86528).
- April 1, 2026: Translate at 640x640 with opset=17 successful! End nodes: /model.23/Concat_4 + /model.23/proto/cv3/act/Mul. HAR 640x640 with proto generated. Quantization in progress (batch_size=4).
- 02 de abril de 2026: Start of YOLO26n-seg compilation campaign at 640x640 with proto included (4 raw outputs: box, score, mask_coef, proto). Model cut in 3 separate outputs before Concat_4 (test_split_compile.sh) to eliminate the concat24 node causing "Agent infeasible".
- 02 de abril de 2026: Error "Performance Flow requires automatic resource utilization" resolved by removing resources_param when using compiler_optimization_level=max. The two commands are incompatible.
- 02 de abril de 2026: compiler_optimization_level=max froze for 10+ min at the first bar. Level 2 also froze. Cause: compiler tried to maximize FPS with aggressive double buffering of proto [1,32,160,160], saturating the partition search.
- 02 de abril de 2026: performance_param(fps=30) resolved the partitioner freeze — forced 60% utilization across all resources (instead of 100%). Partitioner found a solution in 5 contexts after 273 iterations (~10 min). But compilation failed with "PrePostAgent Agent infeasible".
- 02 de abril de 2026: PrePostAgent infeasible = DMA output agent cannot allocate buffer for the proto tensor [1,32,160,160] (~800KB) with the 5-context partition generated. Attempts with output_format and max_context_clusters failed (invalid commands in this DFC version).
- 02 de abril de 2026: Valid resources_param parameters identified via grep in hailo_model_zoo .alls: max_apu_utilization, max_compute_utilization, max_compute_16bit_utilization, max_control_utilization, max_input_aligner_utilization, max_memory_utilization, max_utilization, strategy=greedy.
- 02 de abril de 2026: Attempt with resources_param(strategy=greedy, max_utilization=0.6) in progress — greedy algorithm generates a different partition that may be compatible with PrePost.
- 06 de abril de 2026: Resumed nano campaign. Recompilation attempt with cut_onnx_10outputs.sh (10 outputs) — failed with "matmul1 Agent infeasible" in all combinations (0.6/0.8/0.9, greedy/none, fps=60). The 10-output cut exposes matmul1 in a position requiring double-buffering, not supported by the DFC when the layer has 2 consumers.
- 06 de abril de 2026: Discovery: performance_param(fps=X) is ignored in multi-context models — warning "REQUIRED_FPS is not currently supported for multi context, reverting to MAX_FPS".
- 06 de abril de 2026: Back to test_split_compile.sh (3 outputs). greedy+0.6 → 5 ctx → PrePostAgent infeasible. greedy+0.8 → 4 ctx → PrePostAgent infeasible. greedy+0.9 → 3 ctx → SUCCESS. Mapping in 12m50s, 3 contexts, compilation in 8s. yolo26n_seg_640.hef (9.1 MB) generated with 3-output cut + greedy + 0.9.

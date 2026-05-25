# Hailo-8 PCIe Descriptor Page Size – Problem Study

## 1. Context: how the Hailo-8 connects to the Raspberry Pi 5

The Hailo-8 is an AI accelerator connected to the Raspberry Pi 5 via **PCIe**
(PCI Express). PCIe is a high-speed bus that allows the CPU to communicate
with peripherals such as GPUs, SSDs and AI accelerators.

On the Pi 5, the Hailo-8 is connected via **PCIe Gen 2 x1** — a single data lane
with ~500 MB/s bandwidth.

---

## 2. What is DMA

**DMA (Direct Memory Access)** is a mechanism that allows the Hailo-8 to read and
write directly into the CPU's RAM **without interrupting it for every byte**. Without DMA,
the CPU would have to manually copy each frame to the Hailo — unfeasible at 381 FPS.

With DMA, the data flow is:

```
CPU prepares frame in RAM
        ↓
Hailo reads via DMA (PCIe) → processes → writes result via DMA
        ↓
CPU reads result from RAM
```

---

## 3. What are Descriptors and Descriptor Pages

For DMA to work, the driver creates a **descriptor list** — a table
in memory where each entry tells the Hailo:

> *"The next data block is at memory address X with Y bytes."*

Each entry points to a **memory block (page)** of fixed size —
the `desc_page_size`. It is like a book index: each chapter (descriptor)
points to a section (memory page).

```
Descriptor 0 → [memory page: 16384 bytes] ← part of frame
Descriptor 1 → [memory page: 16384 bytes] ← part of frame
Descriptor 2 → [memory page: 16384 bytes] ← part of frame
...
```

---

## 4. Why HailoRT uses 16384 by default

HailoRT chooses **16384 bytes** because:

- Fewer descriptors are needed per frame (less overhead)
- Fewer PCIe interrupts
- Higher transfer throughput

For a YOLOv8s input frame (640×640×3 ≈ 1.2 MB):

| Page size | Descriptors per frame |
|---|---|
| 16384 bytes | ~75 |
| 4096 bytes | ~300 (4× more) |

---

## 5. Why the AGL kernel limits to 4096

The AGL kernel was compiled for **embedded and automotive systems**, with
conservative memory settings. The limitation comes from the **kernel DMA
subsystem** (`dma_get_max_seg_size`), which in AGL returns 4096 bytes as the
maximum supported size for contiguous DMA mappings.

This is not a bug — it is a deliberate choice to ensure compatibility with
diverse hardware in automotive environments where physical memory may be
fragmented.

---

## 6. What happens exactly during the error

When the `hailo_pci` driver loads, it queries the kernel:

```
"What is the maximum DMA page size you support?"
→ AGL kernel responds: 4096
```

HailoRT then tries to configure 16384-byte descriptors, and the driver
detects the incompatibility:

```
[HailoRT] [error] CHECK failed - max_desc_page_size given 16384 is bigger than hw max desc page size 4096
[HailoRT] [error] CHECK_SUCCESS failed with status=HAILO_INTERNAL_FAILURE(8)
[HailoRT CLI] [error] Failed configure vdevice from hef
```

The driver refuses to proceed because creating descriptors larger than what the
kernel supports would result in **memory corruption** or invalid transfers.

---

## 7. The solution and why it works

**Temporary (for testing):**
```bash
modprobe -r hailo_pci
modprobe hailo_pci force_desc_page_size=4096
```

**Permanent:**
```bash
echo 'options hailo_pci force_desc_page_size=4096' >> /etc/modprobe.d/hailo_pci.conf
reboot
```

The `force_desc_page_size` parameter **forces the driver to use 4096-byte pages**
from the start, matching what the AGL kernel supports. The Hailo-8 hardware
accepts any page size — the limitation was exclusively on the kernel side.

> **Note:** If maximum DMA performance is needed (using 16384-byte pages),
> the solution would be to recompile the AGL kernel with support for larger DMA pages.
> This is out of the current scope but may be considered in a future phase
> if the inference pipeline requires higher throughput.

---

## 8. Performance impact (measured results)

Benchmark run with `hailortcli benchmark /path/to/model.hef` after applying
the fix (`force_desc_page_size=4096`):

| Metric | Value |
|---|---|
| FPS (hw-only) | 398.44 |
| FPS (streaming) | 381.59 |
| HW Latency | 6.71 ms |
| PCIe overhead | ~4.2% |

Despite using 4× more descriptors per frame, the performance impact is
minimal because the true bottleneck is the internal Hailo-8 processing, not
the PCIe transfer. At 381 FPS, a 30 FPS camera uses less than 10% of the
Hailo capacity — leaving margin to run multiple models in parallel
(e.g. object detection + lane detection).

### What each metric means

- **FPS (hw-only):** maximum theoretical chip speed of the Hailo in isolation, excluding
  PCIe transfer time. Defines the hardware ceiling.
- **FPS (streaming):** actual speed including PCIe data transfer
  (input + output). Represents the real pipeline performance.
- **HW Latency:** time the Hailo takes to process a single frame
  internally (~6.71 ms = capable of ~149 FPS response), critical for
  low-latency autonomous driving applications.

---

## 9. Environment

| Component | Details |
|---|---|
| Device | Raspberry Pi 5 |
| OS | AGL (Automotive Grade Linux) |
| AI Module | Hailo-8 AI HAT |
| Interface | PCIe Gen 2 x1 |
| Tested model | YOLOv8s (`yolov8s.hef`) |
| HailoRT fix | `force_desc_page_size=4096` |

---

## References

- [Hailo Community – PCIe max_desc_page_size issue](https://community.hailo.ai/t/pcie-max-desc-page-size-issue/136)
- [Hailo Community – HailoRT error CHECK failed max_desc_page_size](https://community.hailo.ai/t/hailort-error-check-failed-max-desc-page-size-given-16384-is-bigger-than-hw-max-desc-page-size-4096/3690)
- [hailort-drivers – GitHub](https://github.com/hailo-ai/hailort-drivers)
- [Dynamic DMA mapping Guide – Linux Kernel](https://docs.kernel.org/core-api/dma-api-howto.html)

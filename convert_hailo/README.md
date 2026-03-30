# Hailo Conversion Flow (YOLOv8-seg) - Senna Edition

This repository section focuses on the conversion flow for YOLOv8-seg models into **HEF (Hailo Executable Format)**. The current pipeline covers ONNX export, calibration preparation, organization of Docker-shared artifacts, and compilation through the Hailo Model Zoo.

## Getting Started

### Conversion (`.pt` to `.hef`)
The recommended and current entry point is:

```bash
./convert_flow/run_convert.sh
```

This script performs:
- model export to ONNX
- calibration image preparation
- training parameter loading from `args.yaml`, when available
- `nms_config.json` generation
- HEF compilation inside the Hailo container

Notes:
- The official project entry point is `./convert_flow/run_convert.sh`.
- Legacy root-level scripts for ONNX export, calibration preparation, and the old manual Docker flow were removed to avoid duplication and behavioral drift.
- The compilation step depends on the Hailo container being available. During environment setup or recovery, you may need to run `./convert_flow/run_hailo_docker.sh` first.

## Local Configuration

The main scripts support local configuration through a `.env.hailo` file at the project root.

Use the example file as a starting point:

```bash
cp .env.hailo.example .env.hailo
```

Set the absolute paths for your local machine or server in `.env.hailo`, for example:
- `BASE_PROJECT`
- `VENV_NAME`
- `SHARED_DIR`
- `CONTAINER_NAME`
- `DOCKER_IMAGE_NAME`
- `DOCKER_TAR_FILE`

This file is machine-local and should not be published to the public repository.

## External Prerequisites

Before using the Docker-based conversion flow, you need the Hailo AI Software Suite Docker image archive referenced by `DOCKER_TAR_FILE`.

In practice, this means:
- download the Hailo AI Software Suite Docker package from the Hailo Developer Zone
- place the downloaded tar archive where your local `.env.hailo` points to it
- keep `DOCKER_TAR_FILE` aligned with the actual downloaded filename

The Hailo documentation distributed with the suite is also available locally after setup inside `shared_with_docker/doc/`.

## Project Structure

- **`convert_flow/`**: main conversion flow, with scripts and documentation for the recommended pipeline.
- **`shared_with_docker/`**: folder shared with Docker, used to store `best.onnx`, calibration images, helper scripts, `nms_config.json`, and generated compilation artifacts.
- **`docs/`**: supporting documentation and technical context for the project.

Generated `.hef` artifacts are produced in `shared_with_docker/` during compilation and are not meant to be versioned.

## Documentation

The official documentation hub is:

```bash
docs/README.md
```

The `run_convert` flow is documented in a single file:

```bash
docs/01_run_convert.md
```

## Technologies Used

- **Ultralytics YOLOv8**: export and segmentation model structure.
- **Hailo Dataflow Compiler / Hailo Model Zoo**: optimization and HEF compilation.
- **Docker**: isolated environment for the Hailo toolchain.

## Credits

Developed for the ADAS/LKA project, focused on preparing and compiling models for deployment on Hailo hardware.

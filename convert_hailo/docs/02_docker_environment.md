# Docker Environment

This document describes the real behavior of `./convert_flow/run_hailo_docker.sh`.

## Script role

The script:

- loads `.env.hailo` when present
- ensures `shared_with_docker/` exists
- checks whether the Hailo container already exists
- cleans containers stuck in the `created` state
- runs `docker load` if the image is not available yet
- starts or resumes the Hailo container

## Configurable values

Through `.env.hailo`:

- `CONTAINER_NAME`
- `DOCKER_IMAGE_NAME`
- `DOCKER_TAR_FILE`
- `SHARED_DIR`

Current script defaults:

- `CONTAINER_NAME=hailo8_ai_sw_suite_2025-10_container`
- `DOCKER_IMAGE_NAME=hailo8_ai_sw_suite_2025-10:1`
- `DOCKER_TAR_FILE=hailo8_ai_sw_suite_docker_2025-10.tar.gz`

## Required download

`DOCKER_TAR_FILE` refers to the Hailo AI Software Suite Docker archive that must be downloaded separately from the Hailo Developer Zone.

This repository does not contain that tar file. The script only loads it if it is already present on disk.

## How to use

```bash
sudo ./convert_flow/run_hailo_docker.sh
```

## Mounted paths

The script mounts:

- `${SHARED_DIR}` at `/local/shared_with_docker`
- `/dev`
- the Docker socket
- timezone/localtime files
- X11/Xauthority for interactive use when needed

## NVIDIA GPU

When the host has an NVIDIA GPU and `nvidia-container-toolkit`, the script adds:

```bash
--runtime=nvidia --gpus all
```

This is especially important with Docker installed through Snap. Without it, compilation may fall back to CPU.

Sign of incorrect configuration:

```text
[info] No GPU chosen and no suitable GPU found, falling back to CPU.
```

Sign of correct configuration:

```text
[info] No GPU chosen, Selected GPU 0
```

Quick host-side test:

```bash
sudo docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
```

## Note on Docker Snap

When Docker comes from Snap, the script uses a leaner mount configuration to avoid failures in the NVIDIA prestart hook. This path was validated in the current project flow.

## Official Hailo documentation

After the suite is installed and the workspace is initialized, Hailo's bundled documentation can also be found locally under:

```text
shared_with_docker/doc/
```

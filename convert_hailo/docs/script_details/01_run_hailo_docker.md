# Technical Details: `convert_flow/run_hailo_docker.sh`

## Script role

`convert_flow/run_hailo_docker.sh` creates or resumes the Hailo Docker environment used by the main flow.

## Actual behavior

1. Loads `.env.hailo` if present.
2. Resolves:
   - `CONTAINER_NAME`
   - `DOCKER_IMAGE_NAME`
   - `DOCKER_TAR_FILE`
   - `SHARED_DIR`
3. Ensures `SHARED_DIR` exists.
4. Prepares Xauthority for interactive use.
5. Checks whether the container already exists.
6. If the container is in `created`, removes and recreates it.
7. If the image is not loaded yet, runs `docker load`.
8. Mounts `${SHARED_DIR}` at `/local/shared_with_docker`.
9. If an NVIDIA GPU and toolkit are available, adds `--runtime=nvidia --gpus all`.
10. With Docker Snap, uses a reduced mount configuration to avoid failures in the NVIDIA prestart hook.

## Supported environment variables

- `CONTAINER_NAME`
- `DOCKER_IMAGE_NAME`
- `DOCKER_TAR_FILE`
- `SHARED_DIR`

## Real dependencies

- working Docker on the host
- `sudo` access
- image tarball when the image is not yet available locally
- `nvidia-container-toolkit` on the host when GPU-accelerated compilation is expected

## Important note about `DOCKER_TAR_FILE`

`DOCKER_TAR_FILE` points to the Hailo AI Software Suite Docker archive obtained outside this repository, typically from the Hailo Developer Zone.

The script does not download the archive. It only validates its presence and runs `docker load` against the configured path.

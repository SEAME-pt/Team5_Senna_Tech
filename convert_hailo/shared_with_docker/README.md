# `shared_with_docker`

This directory is a runtime workspace shared with the Hailo Docker container.

Generated files created here by `run_convert.sh` include:

- `best.onnx`
- `calibration_images/`
- `nms_config.json`
- `scripts/compile.sh`
- generated `.har`
- generated `.hef`

These files are build/runtime artifacts and should not be versioned.

The directory itself is kept in the repository only to document its purpose.

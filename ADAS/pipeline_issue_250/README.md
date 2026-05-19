# ADAS Pipeline

## Overview
This directory contains the execution pipeline for the ADAS prototype running on the Raspberry Pi and Hailo stack.

The pipeline is being reorganized to keep each module responsible for its own code and local documentation, while cross-cutting architecture notes remain in `docs/`.

## Current Flow
1. `camera`
2. `inference`
3. `post_processing`
4. `LFA`
5. `decision`
6. `external interfaces`

## Entry Points
- `main.py` — legacy integration entry point
- `main2.py` — refactoring entry point used to validate the modular execution flow

## Module Documentation
- [camera](camera/README.md)
- [inference](inference/README.md)

Additional module documentation is still being migrated from `docs/` to the corresponding folders.

## Cross-Cutting Documentation
- [Pipeline interfaces](docs/pipeline_interfaces.md)
- [Architecture proposal](docs/proposta_de_arquitetura.md)

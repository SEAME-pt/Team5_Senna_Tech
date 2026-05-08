# Post-processing Strategy

The current flow compiles the model in raw output mode.

## What this means

Today, `convert_flow/run_convert.sh`:

- generates `nms_config.json`
- compiles the model without integrating hardware-side NMS into `hailomz compile`
- leaves post-processing to the consuming application

## Practical consequence

Post-processing parameters remain adjustable outside the `.hef`, especially:

- confidence threshold
- NMS IoU
- number of classes

## Where this appears in the flow

- `convert_flow/run_convert.sh` generates `shared_with_docker/nms_config.json`
- `convert_flow/scripts/compile.sh` calls `hailomz compile` without `--model-script`

## When to revisit this strategy

It makes sense to revisit this design if the project needs to:

- reduce CPU load during post-processing
- freeze NMS parameters inside the final artifact
- migrate to a flow with post-processing more tightly coupled to the Hailo compiler

Today, the official documentation assumes only the raw output mode that is actually implemented.

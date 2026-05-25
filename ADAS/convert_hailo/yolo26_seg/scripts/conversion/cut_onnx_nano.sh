#!/bin/bash

# ==============================================================================
# ONNX CUT - 3 separate outputs (bbox + score + mask_coef + proto)
# ==============================================================================
# This script runs INSIDE the Hailo Docker container.
# Cuts the ONNX before Concat_4, exposing the 3 separate tensors per concatenated
# scale + proto. Used for yolo26n-seg (nano).
#
# Difference from other cuts:
#   cut_onnx.sh       -> 2 outputs: det[1,37,8400] + proto  (concat24 infeasible)
#   cut_onnx_nano.sh  -> 4 outputs: bbox + score + mask_coef + proto  (this)
#   cut_onnx_small.sh -> 10 outputs: cv2/cv3/cv4 per scale + proto    (matmul1 infeasible on nano)
#
# Usage:
#   bash cut_onnx_nano.sh <input_size>
#
# Example:
#   bash cut_onnx_nano.sh 640
#
# Input:  best.onnx
# Output: best_cut.onnx

INPUT_SIZE="${1:-640}"
DIR_BASE="/local/shared_with_docker"
ONNX_IN="${DIR_BASE}/best.onnx"
ONNX_OUT="${DIR_BASE}/best_cut.onnx"

NUM_ANCHORS=$(python3 -c "s=${INPUT_SIZE}; print((s//8)**2 + (s//16)**2 + (s//32)**2)")

echo "--------------------------------------------------"
echo "ONNX Cut - 3 separate outputs (bbox + score + mask_coef + proto)"
echo "Input:      ${ONNX_IN}"
echo "Output:     ${ONNX_OUT}"
echo "Input size: ${INPUT_SIZE}x${INPUT_SIZE}"
echo "Anchors:    ${NUM_ANCHORS}"
echo "--------------------------------------------------"

if [ ! -f "${ONNX_IN}" ]; then
    echo "ERROR: ONNX not found at ${ONNX_IN}"
    exit 1
fi

python3 << PYEOF
import onnx
from onnx import TensorProto, shape_inference
import os

ONNX_IN  = "${ONNX_IN}"
ONNX_OUT = "${ONNX_OUT}"
NUM_ANCHORS = ${NUM_ANCHORS}

print("Loading ONNX...")
m = onnx.load(ONNX_IN)
m = shape_inference.infer_shapes(m)
print(f"  Nodes in model: {len(m.graph.node)}")

# Find inputs of Concat_4
concat4_inputs = None
for n in m.graph.node:
    if n.name == "/model.23/Concat_4":
        concat4_inputs = list(n.input)
        break

if concat4_inputs is None:
    print("ERROR: /model.23/Concat_4 not found!")
    exit(1)

print(f"  Concat_4 inputs: {concat4_inputs}")

# Shapes of inputs
shape_map = {}
for vi in m.graph.value_info:
    if vi.name in concat4_inputs:
        dims = [d.dim_value for d in vi.type.tensor_type.shape.dim]
        shape_map[vi.name] = dims

for name, shape in shape_map.items():
    print(f"  Output: {name} shape={shape}")

# Create separate outputs
new_outputs = []
for inp_name in concat4_inputs:
    if inp_name in shape_map:
        out = onnx.helper.make_tensor_value_info(inp_name, TensorProto.FLOAT, shape_map[inp_name])
        new_outputs.append(out)

# Keep proto
keep_proto = [o for o in m.graph.output if o.name == "output1"][0]

while len(m.graph.output) > 0:
    m.graph.output.pop()
for out in new_outputs:
    m.graph.output.append(out)
m.graph.output.append(keep_proto)

# Remove Concat_4 + everything downstream
nodes_to_remove = set()

def mark_downstream(output_name):
    for n in m.graph.node:
        if output_name in list(n.input) and n.name not in nodes_to_remove:
            nodes_to_remove.add(n.name)
            for o in n.output:
                mark_downstream(o)

nodes_to_remove.add("/model.23/Concat_4")
mark_downstream("/model.23/Concat_4_output_0")

# Clean up orphans
used = set()
for n in m.graph.node:
    if n.name not in nodes_to_remove:
        used.update(n.input)
for o in m.graph.output:
    used.add(o.name)
for n in m.graph.node:
    if n.name not in nodes_to_remove:
        if not any(o in used for o in n.output):
            nodes_to_remove.add(n.name)

nodes_before = len(m.graph.node)
new_nodes = [n for n in m.graph.node if n.name not in nodes_to_remove]
while len(m.graph.node) > 0:
    m.graph.node.pop()
for n in new_nodes:
    m.graph.node.append(n)

print(f"\nSummary:")
print(f"  Nodes before:    {nodes_before}")
print(f"  Nodes removed:   {nodes_before - len(m.graph.node)}")
print(f"  Nodes remaining: {len(m.graph.node)}")
print(f"  Total outputs:   {len(m.graph.output)}")

onnx.checker.check_model(m)
print("  Validation OK")

onnx.save(m, ONNX_OUT)
size_orig = os.path.getsize(ONNX_IN) / (1024*1024)
size_cut  = os.path.getsize(ONNX_OUT) / (1024*1024)
print(f"  Original: {size_orig:.1f} MB")
print(f"  Cut:      {size_cut:.1f} MB")

print("\n--------------------------------------------------")
print(f"OK: {ONNX_OUT} with 4 outputs (3 heads + proto)")
print("--------------------------------------------------")
PYEOF

exit $?

#!/bin/bash

# ==============================================================================
# ONNX CUT - 10 separate outputs (9 heads + proto)
# ==============================================================================
# This script runs INSIDE the Hailo Docker container.
# Cuts the YOLO26s-seg exposing the 9 final nodes of each scale/type separately
# (one2one_cv2.x, one2one_cv3.x, one2one_cv4.x) + proto, without any concatenation.
#
# Motivation: the Concat_4 approach (4 outputs) fails with PrePostAgent infeasible
# because the tensor [1,37,8400] is too large for the Hailo-8 DMA in multi-context mode.
# With 10 smaller outputs (e.g. [1,64,80,80]) the PrePostAgent has less pressure.
#
# End nodes used:
#   cv2.0 -> bbox stride 8  (80x80)    cv2.1 -> bbox stride 16  (40x40)    cv2.2 -> bbox stride 32  (20x20)
#   cv3.0 -> score stride 8 (80x80)    cv3.1 -> score stride 16 (40x40)    cv3.2 -> score stride 32 (20x20)
#   cv4.0 -> mask stride 8  (80x80)    cv4.1 -> mask stride 16  (40x40)    cv4.2 -> mask stride 32  (20x20)
#   proto -> base masks     (160x160)
#
# Post-processing: manually concatenate the 3 scales of each type before NMS.
#
# Usage:
#   bash cut_onnx_small.sh <input_size>
#
# Examples:
#   bash cut_onnx_small.sh 640
#
# Input:  best.onnx     (original, exported with opset=17)
# Output: best_cut.onnx (10 outputs, ready for translate_onnx_model)

INPUT_SIZE="${1:-640}"
DIR_BASE="/local/shared_with_docker"
ONNX_IN="${DIR_BASE}/best.onnx"
ONNX_OUT="${DIR_BASE}/best_cut.onnx"

echo "--------------------------------------------------"
echo "ONNX Cut - 10 separate outputs (9 heads + proto)"
echo "Input:      ${ONNX_IN}"
echo "Output:     ${ONNX_OUT}"
echo "Input size: ${INPUT_SIZE}x${INPUT_SIZE}"
echo "--------------------------------------------------"

if [ ! -f "${ONNX_IN}" ]; then
    echo "ERROR: ONNX not found at ${ONNX_IN}"
    exit 1
fi

python3 << PYEOF
import onnx
from onnx import TensorProto, shape_inference
import os

ONNX_IN   = "/local/shared_with_docker/best.onnx"
ONNX_OUT  = "/local/shared_with_docker/best_cut.onnx"
INPUT_SIZE = ${INPUT_SIZE}

# Final nodes of each detection head (last Conv of each scale)
END_NODES = [
    "/model.23/one2one_cv2.0/one2one_cv2.0.2/Conv",
    "/model.23/one2one_cv2.1/one2one_cv2.1.2/Conv",
    "/model.23/one2one_cv2.2/one2one_cv2.2.2/Conv",
    "/model.23/one2one_cv3.0/one2one_cv3.0.2/Conv",
    "/model.23/one2one_cv3.1/one2one_cv3.1.2/Conv",
    "/model.23/one2one_cv3.2/one2one_cv3.2.2/Conv",
    "/model.23/one2one_cv4.0/one2one_cv4.0.2/Conv",
    "/model.23/one2one_cv4.1/one2one_cv4.1.2/Conv",
    "/model.23/one2one_cv4.2/one2one_cv4.2.2/Conv",
]

print("Loading ONNX...")
m = onnx.load(ONNX_IN)
print(f"  Nodes in model: {len(m.graph.node)}")

print("Inferring shapes...")
m = shape_inference.infer_shapes(m)

# Map node name -> output name
node_output_map = {}
for n in m.graph.node:
    if n.name in END_NODES:
        node_output_map[n.name] = n.output[0]

print(f"\nNodes found: {len(node_output_map)}/{len(END_NODES)}")
for name, out in node_output_map.items():
    print(f"  {name} -> {out}")

if len(node_output_map) != len(END_NODES):
    missing = [n for n in END_NODES if n not in node_output_map]
    print(f"ERROR: Nodes not found: {missing}")
    exit(1)

# Infer output shapes
shape_map = {}
for vi in list(m.graph.value_info) + list(m.graph.output):
    shape_map[vi.name] = [d.dim_value for d in vi.type.tensor_type.shape.dim]

# Build new outputs
new_outputs = []
for node_name in END_NODES:
    out_name = node_output_map[node_name]
    shape = shape_map.get(out_name, None)
    if shape:
        out = onnx.helper.make_tensor_value_info(out_name, TensorProto.FLOAT, shape)
    else:
        out = onnx.helper.make_tensor_value_info(out_name, TensorProto.FLOAT, None)
    new_outputs.append(out)
    print(f"  Output: {out_name} shape={shape}")

# Add proto
proto_out = [o for o in m.graph.output if o.name == "output1"]
if not proto_out:
    print("ERROR: output1 (proto) not found!")
    exit(1)
new_outputs.append(proto_out[0])
print(f"  Output: output1 (proto)")

# Replace outputs
while len(m.graph.output) > 0:
    m.graph.output.pop()
for out in new_outputs:
    m.graph.output.append(out)

# Remove nodes downstream of end nodes (Concat_4, Tiles, etc.)
# Mark end node outputs as "terminals"
terminal_outputs = set(node_output_map.values())
terminal_outputs.add("output1")

nodes_to_remove = set()

def mark_downstream(output_name):
    for n in m.graph.node:
        if output_name in list(n.input) and n.name not in nodes_to_remove:
            # Do not remove if node is one of the end nodes
            if n.name not in END_NODES:
                nodes_to_remove.add(n.name)
                for o in n.output:
                    mark_downstream(o)

for out_name in terminal_outputs:
    mark_downstream(out_name)

print(f"\nNodes to remove (downstream): {len(nodes_to_remove)}")
for name in sorted(nodes_to_remove):
    print(f"  - {name}")

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

print("\nValidating model...")
onnx.checker.check_model(m)
print("  Validation OK")

print("\nSaving...")
onnx.save(m, ONNX_OUT)

size_orig = os.path.getsize(ONNX_IN) / (1024*1024)
size_cut  = os.path.getsize(ONNX_OUT) / (1024*1024)
print(f"  Original: {size_orig:.1f} MB")
print(f"  Cut:      {size_cut:.1f} MB")

print("\n--------------------------------------------------")
print(f"OK: {ONNX_OUT} with 10 outputs")
print("--------------------------------------------------")
PYEOF

exit $?

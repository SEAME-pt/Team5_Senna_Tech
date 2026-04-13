#!/bin/bash

# ==============================================================================
# ONNX CUT - Removes end-to-end post-processing (Tiles)
# ==============================================================================
# This script runs INSIDE the Hailo Docker container.
# Removes the Tile/Gather/GatherElements nodes from YOLO26s-seg that the Hailo DFC
# does not support. Cuts at Concat_4 (raw detections before top-k).
# Keeps the proto branch (output1) for mask generation.
#
# Usage:
#   bash cut_onnx.sh <input_size>
#
# Examples:
#   bash cut_onnx.sh 416     ->  concat24 [1,37,3549]
#   bash cut_onnx.sh 640     ->  concat24 [1,37,8400]
#
# Input:  best.onnx        (original, with Tiles) - export with opset=17
# Output: best_cut.onnx   (without Tiles, ready for translate_onnx_model)
#
# IMPORTANT: export ONNX with opset=17 to fix attention shapes:
#   yolo export model=best.pt format=onnx simplify=true imgsz=640 opset=17
# With opset=12 the attention Reshape at /model.10/m/m.0/attn/Reshape fails with
# incompatible shapes ({1,512,20,20} -> {1,4,128,256}).

INPUT_SIZE="${1:-416}"
DIR_BASE="/local/shared_with_docker"
ONNX_IN="${DIR_BASE}/best.onnx"
ONNX_OUT="${DIR_BASE}/best_cut.onnx"

echo "--------------------------------------------------"
echo "ONNX Cut - Removing post-processing (Tiles)"
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

# Number of anchors: sum of grids at 3 scales (stride 8, 16, 32)
NUM_ANCHORS = (INPUT_SIZE//8)**2 + (INPUT_SIZE//16)**2 + (INPUT_SIZE//32)**2
print(f"Input size: {INPUT_SIZE}x{INPUT_SIZE} -> {NUM_ANCHORS} anchors")

print("Loading ONNX...")
m = onnx.load(ONNX_IN)
print(f"  Nodes in model: {len(m.graph.node)}")
print(f"  Original outputs: {[o.name for o in m.graph.output]}")

print("\nInferring shapes...")
m = shape_inference.infer_shapes(m)

# Detect number of channels in Concat_4 (37 for s, 38 for n, etc.)
NUM_CHANNELS = None
for vi in m.graph.value_info:
    if vi.name == "/model.23/Concat_4_output_0":
        NUM_CHANNELS = vi.type.tensor_type.shape.dim[1].dim_value
        break
if NUM_CHANNELS is None:
    # Fallback: end-to-end output0 has 1 extra field (class_id) vs Concat_4 raw
    # end-to-end: bbox(4) + score(1) + class_id(1) + mask(32) = 38
    # Concat_4:   bbox(4) + class_score(nc) + mask(32) = 37 (with nc=1)
    for o in m.graph.output:
        if o.name == "output0":
            NUM_CHANNELS = o.type.tensor_type.shape.dim[2].dim_value - 1
            break
if NUM_CHANNELS is None:
    NUM_CHANNELS = 37
print(f"Detected channels: {NUM_CHANNELS}")

# New output: Concat_4
new_output = onnx.helper.make_tensor_value_info(
    "/model.23/Concat_4_output_0",
    TensorProto.FLOAT,
    [1, NUM_CHANNELS, NUM_ANCHORS]
)

# Keep output1 (proto), remove output0 (post-tile)
keep_output1 = [o for o in m.graph.output if o.name == "output1"][0]

while len(m.graph.output) > 0:
    m.graph.output.pop()
m.graph.output.append(new_output)
m.graph.output.append(keep_output1)

print("\nIdentifying nodes to remove...")

# Identify nodes downstream of Tiles
nodes_to_remove = set()

def mark_downstream(output_name):
    for n in m.graph.node:
        if output_name in list(n.input) and n.name not in nodes_to_remove:
            nodes_to_remove.add(n.name)
            for o in n.output:
                mark_downstream(o)

for n in m.graph.node:
    if n.op_type == "Tile":
        nodes_to_remove.add(n.name)
        for o in n.output:
            mark_downstream(o)

print(f"  Nodes downstream of Tiles: {len(nodes_to_remove)}")
for name in sorted(nodes_to_remove):
    print(f"    - {name}")

# Outputs used by remaining nodes
used_by_remaining = set()
for n in m.graph.node:
    if n.name not in nodes_to_remove:
        used_by_remaining.update(n.input)
for o in m.graph.output:
    used_by_remaining.add(o.name)

# Orphan nodes: output only used by removed nodes
orphans = set()
for n in list(m.graph.node):
    if n.name not in nodes_to_remove:
        outputs_used = any(o in used_by_remaining for o in n.output)
        if not outputs_used:
            orphans.add(n.name)

print(f"  Orphan nodes (only fed Tiles): {len(orphans)}")
for name in sorted(orphans):
    print(f"    - {name}")

nodes_to_remove.update(orphans)

# Remove nodes
nodes_before = len(m.graph.node)
new_nodes = [n for n in m.graph.node if n.name not in nodes_to_remove]
while len(m.graph.node) > 0:
    m.graph.node.pop()
for n in new_nodes:
    m.graph.node.append(n)

print(f"\nSummary:")
print(f"  Nodes before:   {nodes_before}")
print(f"  Nodes removed:  {nodes_before - len(m.graph.node)}")
print(f"  Nodes remaining:{len(m.graph.node)}")
print(f"  Outputs: {[o.name for o in m.graph.output]}")

print("\nValidating model...")
onnx.checker.check_model(m)
print("  Validation OK")

print("\nSaving...")
onnx.save(m, ONNX_OUT)

size_orig = os.path.getsize(ONNX_IN) / (1024*1024)
size_cut = os.path.getsize(ONNX_OUT) / (1024*1024)
print(f"  Original: {size_orig:.1f} MB")
print(f"  Cut:      {size_cut:.1f} MB")

print("\n--------------------------------------------------")
print(f"OK: {ONNX_OUT}")
print("--------------------------------------------------")
PYEOF

exit $?

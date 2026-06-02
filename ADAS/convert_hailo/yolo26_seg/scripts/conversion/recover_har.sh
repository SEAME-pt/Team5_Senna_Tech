#!/bin/bash

# ==============================================================================
# HAR RECOVERY FROM WORK_DIR (post-QFT)
# ==============================================================================
# Runs INSIDE the Hailo Docker container.
# Rebuilds the quantized HAR by replacing the .hn and .npz of the original HAR
# with the post-QFT weights saved in the work_dir, skipping noise analysis.
#
# Usage:
#   bash recover_har.sh <model_name>
#
# Example:
#   bash recover_har.sh yolo26s_seg_640

MODEL_NAME="${1:-yolo26s_seg_640}"
DIR_BASE="/local/shared_with_docker"
HAR="${DIR_BASE}/${MODEL_NAME}.har"
QHAR="${DIR_BASE}/${MODEL_NAME}_quantized.har"
WORK_DIR="/tmp/hailo_workdir_${MODEL_NAME}/quantization-aware_fine-tuning"

echo "--------------------------------------------------"
echo "HAR recovery from work_dir (post-QFT)"
echo "Model:    ${MODEL_NAME}"
echo "HAR:      ${HAR}"
echo "Work dir: ${WORK_DIR}"
echo "Output:   ${QHAR}"
echo "--------------------------------------------------"

if [ ! -f "${HAR}" ]; then
    echo "ERROR: Original HAR not found at ${HAR}"
    exit 1
fi

if [ ! -d "${WORK_DIR}" ]; then
    echo "ERROR: work_dir not found at ${WORK_DIR}"
    exit 1
fi

python3 << PYEOF
import h5py, numpy as np, tarfile, io, os, tempfile, inspect
from hailo_sdk_client import ClientRunner

# ------------------------------------------------------------------
# Inspect load_har to understand ParamsKinds logic
# ------------------------------------------------------------------
print("=== Source of load_har (relevant parts) ===")
src = inspect.getsource(ClientRunner.load_har)
for line in src.split('\n'):
    if any(k in line for k in ['params_kind', 'ParamsKind', 'state', 'NATIVE', 'quantized', 'hailo_opt']):
        print(" ", line)

print("\n=== Valid runner states ===")
try:
    from hailo_sdk_common.states.states import HailoModelState
    print(list(HailoModelState))
except Exception as e:
    print(f"  {e}")


HAR      = "${HAR}"
WORK_DIR = "${WORK_DIR}"
HDF5     = f"{WORK_DIR}/acceleras.hdf5"
HN_QFT   = f"{WORK_DIR}/acceleras_model.hn"
QHAR     = "${QHAR}"
MODEL    = "${MODEL_NAME}"

# ------------------------------------------------------------------
# Load original NPZ from HAR
# ------------------------------------------------------------------
print("Loading original NPZ...")
t = tarfile.open(HAR)
npz_data = np.load(io.BytesIO(t.extractfile(f"{MODEL}.npz").read()), allow_pickle=True)
npz_keys = list(npz_data.keys())
print(f"  {len(npz_keys)} keys in original NPZ")

# ------------------------------------------------------------------
# Load post-QFT weights from HDF5
# ------------------------------------------------------------------
print("Loading post-QFT weights from HDF5...")
hdf5_weights = {}
with h5py.File(HDF5, 'r') as f:
    def collect(name, obj):
        if isinstance(obj, h5py.Dataset):
            hdf5_weights[name] = obj[()]
    f.visititems(collect)
print(f"  {len(hdf5_weights)} entries in HDF5")

# ------------------------------------------------------------------
# Build new NPZ with ALL HDF5 entries (hailo_optimized format)
# ------------------------------------------------------------------
print("Building new NPZ with all HDF5 entries (hailo_optimized)...")
new_npz = hdf5_weights  # 16548 complete post-QFT entries
print(f"  Total entries: {len(new_npz)}")

# Save new NPZ to temporary file
tmp_npz = tempfile.mktemp(suffix=".npz")
np.savez(tmp_npz, **new_npz)
tmp_npz_real = tmp_npz + ".npz" if not tmp_npz.endswith(".npz") else tmp_npz
if not os.path.exists(tmp_npz_real):
    tmp_npz_real = tmp_npz
print(f"  Temporary NPZ: {tmp_npz_real} ({os.path.getsize(tmp_npz_real)/1024/1024:.1f} MB)")

# ------------------------------------------------------------------
# Build new HAR tar: replace .hn and .npz
# ------------------------------------------------------------------
print("\nBuilding new HAR...")
with tarfile.open(QHAR, "w") as out:
    for member in t.getmembers():
        name = member.name
        if name == f"{MODEL}.npz":
            # replace with post-QFT NPZ
            out.add(tmp_npz_real, arcname=name)
            print(f"  {name} -> post-QFT NPZ")
        elif name == f"{MODEL}.hn":
            # replace with post-QFT .hn
            out.add(HN_QFT, arcname=name)
            print(f"  {name} -> post-QFT HN")
        elif name == f"{MODEL}.metadata.json":
            # copy original unchanged
            data = t.extractfile(member)
            out.addfile(member, data)
            print(f"  {name} -> original")
        else:
            # other files: copy from original
            data = t.extractfile(member)
            if data:
                out.addfile(member, data)
            else:
                out.addfile(member)
            print(f"  {name} -> original")

os.unlink(tmp_npz_real)

size = os.path.getsize(QHAR) / (1024*1024)
print(f"\nOK: {QHAR} ({size:.1f} MB)")

# ------------------------------------------------------------------
# Verify by loading with ClientRunner
# ------------------------------------------------------------------
print("\nVerifying with ClientRunner...")
from hailo_sdk_client import ClientRunner
runner = ClientRunner(har=QHAR)
print("  Runner loaded OK")
runner.save_har(QHAR)
print(f"  HAR re-saved OK: {os.path.getsize(QHAR)/1024/1024:.1f} MB")
PYEOF

exit $?

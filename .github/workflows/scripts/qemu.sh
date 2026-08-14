#!/bin/bash
# QEMU startup script for CI (runs in screen session)
# Usage: qemu.sh <image_path> [firmware_dir]

IMAGE="${1:-openruyi-virt_riscv64.qcow2}"
FW_DIR="${2:-.}"

START_PORT=12060
PORT=$START_PORT
while ss -tln 2>/dev/null | grep -qE ":${PORT}\b" || \
      netstat -tln 2>/dev/null | grep -qE ":${PORT}\b"; do
    ((PORT++))
done

# Write port to file so CI can discover it
echo "$PORT" > "${FW_DIR}/ssh_port.txt"

QEMU_CMD="qemu-system-riscv64"
VM_ARGS="-nographic -machine virt,pflash0=pflash0,pflash1=pflash1 \
  -smp 4 -m 12G \
  -cpu rva23s64 \
  -blockdev node-name=pflash0,driver=file,read-only=on,filename=${FW_DIR}/RISCV_VIRT_CODE.fd \
  -blockdev node-name=pflash1,driver=file,filename=${FW_DIR}/RISCV_VIRT_VARS.fd \
  -drive file=${IMAGE},format=qcow2,id=hd0,if=none \
  -object rng-random,filename=/dev/urandom,id=rng0 \
  -device virtio-rng-device,rng=rng0 \
  -device virtio-blk-device,drive=hd0 \
  -device virtio-net-device,netdev=usernet \
  -netdev user,id=usernet,hostfwd=tcp::${PORT}-:22"

echo "Starting: $QEMU_CMD $VM_ARGS"
exec $QEMU_CMD $VM_ARGS

#!/bin/bash
# Run the resizer benchmark on the KV260 board.
# Usage: bash run.sh
# Run from this machine (not on the board) — it copies and executes remotely.

BOARD="ubuntu@192.168.68.60"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Copying benchmark script to board..."
scp "$SCRIPT_DIR/resizer_benchmark.py" $BOARD:/tmp/resizer_benchmark.py

echo "Running on board..."
ssh $BOARD "sudo bash -c 'XILINX_XRT=/usr BOARD=KV260 /usr/local/share/pynq-venv/bin/python3 /tmp/resizer_benchmark.py 2>&1'"

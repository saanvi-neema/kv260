# KV260 Key Learnings

Things we figured out the hard way — so we don't have to again.

---

## DPU vs ARM Performance (Resizer IP)

**Task:** 4K (3840×2160) → 1080p bilinear image resize, 20 runs each

| Metric | DPU | ARM Processor |
|---|---|---|
| Mean (ms) | **66.7** | 380.6 |
| Std dev (ms) | **±0.2** | ±0.9 |
| Min (ms) | 66.5 | 378.8 |
| Max (ms) | 67.1 | 382.4 |
| FPS | **15.0** | 2.6 |
| Speedup | **5.70×** | baseline |

- DPU is **5.7× faster** and far more consistent
- The 247ms figure in the original notebook was a cold/single run — steady-state is 66.7ms
- DPU std dev is only ±0.2ms — essentially deterministic

---

## How to Run the Resizer Benchmark

```bash
bash resizer/run.sh
```

Or manually:
```bash
scp resizer/resizer_benchmark.py ubuntu@192.168.68.60:/tmp/
ssh ubuntu@192.168.68.60 "sudo bash -c 'XILINX_XRT=/usr BOARD=KV260 /usr/local/share/pynq-venv/bin/python3 /tmp/resizer_benchmark.py 2>&1'"
```

**Why `XILINX_XRT=/usr`?** PYNQ throws "No Devices Found" without this env var set.  
**Why `sudo`?** PYNQ needs root to program the DPU and access `/dev/dri/`.  
**Why change directory?** `resizer.bit` and `images/` are resolved relative to the notebook folder.

---

## PYNQ Environment

- Python env: `/usr/local/share/pynq-venv/`
- Source env: `source /etc/profile.d/pynq_venv.sh`
- Key env vars: `XILINX_XRT=/usr`, `BOARD=KV260`
- Jupyter root: `/root/jupyter_notebooks/`
- Jupyter port: 9090, password: `xilinx`

---

## DPU Config

- We use **B512** — it is the default bundled with pynq-dpu
- B512 bitstream location: `/usr/local/share/pynq-venv/lib/python3.10/site-packages/pynq_dpu/dpu.bit`
- Do **not** use B4096 — requires extra setup and not needed
- `pynq_dpu` must always be run from **Jupyter** — not SSH terminal (silent hang)

---

## DPU Sanity Checks (run before any DPU work)

```bash
# Check 1 — pynq_dpu import (safe in SSH, no hardware access)
source /etc/profile.d/pynq_venv.sh
python3 -c "from pynq_dpu import DpuOverlay; print('pynq_dpu OK')"

# Check 2 — DPU firmware loaded (expect: 1)
cat /sys/bus/platform/devices/axi:zyxclmm_drm/kds_numcus

# Check 3 — CMA memory (expect: CmaFree > 500000 kB)
cat /proc/meminfo | grep Cma

# Check 4 — xbutil device ready
sudo xbutil examine 2>&1 | grep "Device Ready"
```

---

## Face Detection Robot

- App: `/home/ubuntu/cnn-demo/kria_app.py`
- Runs on port 5000: `http://kria.local:5000`
- Uses OpenCV Haar Cascade — not the DPU
- Servo sweeps 0→90→180→90→0° when face detected, 10s cooldown
- Serial to Elegoo Mega at 9600 baud on `/dev/ttyACM0`

**Every reboot:**
```bash
sudo chmod 666 /dev/ttyACM0 /dev/video0 /dev/video1
cd /home/ubuntu/cnn-demo
/home/ubuntu/vitis-env/bin/python3 -u kria_app.py > /tmp/kria_app.txt 2>&1 &
```

---

## SSH Key Setup (first time from a new machine)

The board resets SSH known_hosts after reboot. If you get host key errors:

```bash
ssh-keygen -R 192.168.68.60
ssh -o StrictHostKeyChecking=accept-new ubuntu@192.168.68.60
```

To avoid password prompts (set up key auth):
```bash
# On your machine — generate key if needed
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""

# On the board — paste your public key
mkdir -p ~/.ssh
echo "YOUR_PUBLIC_KEY" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
```

---

## What's Next

| Idea | Notes |
|---|---|
| Face-tracking servo | Map face X position on screen → servo angle |
| Remote control UI | Add arrow buttons to kria_app.py web UI |
| Robot chassis | Motor shield + chassis ordered from Amazon |
| YOLO on DPU | Flash Ubuntu 22.04 → run YOLO at 30fps |
| Face counter | Log detections over time, show on web UI |

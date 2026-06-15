# KV260 — AMD Kria Development Board

Projects, benchmarks, setup guides, and learnings for the AMD Kria KV260 board.

---

## Hardware

| Component | Details |
|---|---|
| Board | AMD Kria KV260 Vision AI Starter Kit |
| IP | 192.168.68.60 |
| Hostname | kria / kria.local |
| OS | Ubuntu 24.04 LTS |
| DPU config | B512 (via Kria-PYNQ) |
| Attached | Elegoo Mega 2560, SG90 Servo, Logitech USB Webcam |

---

## SSH Access

```bash
ssh ubuntu@192.168.68.60
# password: amdkria
```

Jupyter runs automatically on boot:
```
http://192.168.68.60:9090   password: xilinx
```

---

## Repo Structure

```
kv260/
├── README.md              — this file
├── DPU_setup.md           — full DPU setup guide (Ubuntu 22.04 + Kria-PYNQ)
├── ONBOARDING.md          — face detection robot setup and how it works
├── LEARNINGS.md           — key findings and gotchas from sessions
└── resizer/
    ├── README.md          — resizer benchmark docs and results
    ├── resizer_benchmark.py  — benchmark script (runs on board)
    └── run.sh             — one-command launcher from this machine
```

---

## Projects

### Face Detection Robot
Live face detection via USB webcam. When a face is detected, an SG90 servo sweeps automatically. Controlled from any browser on the same WiFi.

- See `ONBOARDING.md` for full setup and how it works
- App: `/home/ubuntu/cnn-demo/kria_app.py`
- Start: `ssh ubuntu@192.168.68.60` then follow startup steps in ONBOARDING.md

### Resizer Benchmark (DPU vs ARM)
Benchmarks the hardware-accelerated image resizer IP running on the KV260's DPU against the ARM CPU doing the same task in software.

- See `resizer/`
- Result: **DPU is 5.7× faster** (66.7ms vs 380.6ms for 4K→1080p)

---

## Key Benchmarks

| Task | DPU | ARM | Speedup |
|---|---|---|---|
| 4K→1080p bilinear resize | 66.7ms ±0.2 | 380.6ms ±0.9 | **5.70×** |
| YOLOv3 inference (B512) | ~150ms | ~83ms (MobileNetV2) | — |

---

## Important Rules

- Always use `/usr/local/share/pynq-venv/bin/python3` — not system Python
- `pynq_dpu` must run from **Jupyter only** — silent hang in SSH terminal
- Run `sudo chmod 666 /dev/ttyACM0 /dev/video0 /dev/video1` after every reboot
- Do not use `apt install vitis-ai-runtime` — broken on Ubuntu 24.04 kernel
- We use **B512 DPU config** — not B4096

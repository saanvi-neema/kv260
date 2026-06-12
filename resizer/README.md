# KV260 Resizer — DPU vs ARM Benchmark

Benchmarks the hardware-accelerated image resizer IP on the KV260's DPU
against the ARM CPU doing the same task in software.

---

## Benchmark Results (KV260 revB, Ubuntu 24.04, B512 DPU config, n=20)

| Metric | DPU | ARM |
|---|---|---|
| Mean (ms) | **66.7** | 380.6 |
| Std dev (ms) | **±0.2** | ±0.9 |
| Min (ms) | 66.5 | 378.8 |
| Max (ms) | 67.1 | 382.4 |
| FPS | **15.0** | 2.6 |
| Speedup | **5.70×** | baseline |

**DPU is 5.7× faster** and nearly deterministic (±0.2ms std dev).

> Note: The 247ms figure in the original Jupyter notebook was a cold/single run.
> Real steady-state performance is 66.7ms.

---

## How to Run

### One-liner (from this machine)

```bash
bash run.sh
```

### Manually

```bash
scp resizer_benchmark.py ubuntu@192.168.68.60:/tmp/
ssh ubuntu@192.168.68.60 \
  "sudo bash -c 'XILINX_XRT=/usr BOARD=KV260 \
  /usr/local/share/pynq-venv/bin/python3 /tmp/resizer_benchmark.py 2>&1'"
```

### Or in Jupyter

Open `http://192.168.68.60:9090/lab/tree/pynq-helloworld/resizer_pl.ipynb` (password: `xilinx`) and run all cells.

---

## How It Works

```
resizer_benchmark.py
│
├── Overlay("resizer.bit")          — loads DPU bitstream
├── allocate()                      — allocates shared ARM+DPU memory (CMA)
├── in_buffer[:] = image            — copies 4K image into shared memory
│
├── run_kernel() x20  [DPU path]
│     dma.sendchannel → DPU         — streams image to DPU over AXI DMA
│     resizer.write(0x81)           — triggers the resize IP
│     dma.recvchannel ← DU         — streams result back to ARM
│
├── image.resize() x20  [ARM path]  — PIL bilinear (software, for comparison)
│
└── prints results table
```

---

## Key Files on the Board

| Path | What it is |
|---|---|
| `/root/jupyter_notebooks/pynq-helloworld/resizer.bit` | DPU bitstream for the resizer IP |
| `/root/jupyter_notebooks/pynq-helloworld/resizer.hwh` | Hardware description file |
| `/root/jupyter_notebooks/pynq-helloworld/images/sahara.jpg` | Test image (4K, ~25MB) |
| `/root/jupyter_notebooks/pynq-helloworld/resizer_pl.ipynb` | Original Jupyter notebook |

---

## Important Notes

- **Must run as root** — PYNQ needs root to program the DPU and access `/dev/dri/`
- **`XILINX_XRT=/usr` must be set** — otherwise PYNQ throws "No Devices Found"
- **Working directory must be the notebook folder** — `resizer.bit` and `images/` are relative paths
- The resizer IP works fine over SSH as root (unlike `pynq_dpu` which must run from Jupyter)

---

## Files

| File | Purpose |
|---|---|
| `resizer_benchmark.py` | Benchmark script — copy to board and run |
| `run.sh` | One-command launcher from this machine |
| `README.md` | This file |

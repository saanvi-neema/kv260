import sys, os
os.chdir("/root/jupyter_notebooks/pynq-helloworld")

from PIL import Image
import numpy as np
import time
from pynq import allocate, Overlay

print("Loading resizer.bit overlay...", flush=True)
resize_design = Overlay("resizer.bit")
dma     = resize_design.axi_dma_0
resizer = resize_design.resize_accel_0
print("Overlay loaded.", flush=True)

original_image = Image.open("images/sahara.jpg")
old_width, old_height = original_image.size
print(f"Image: {old_width}x{old_height}", flush=True)

new_width  = old_width  // 2
new_height = old_height // 2

in_buffer  = allocate(shape=(old_height, old_width, 3), dtype=np.uint8, cacheable=1)
out_buffer = allocate(shape=(new_height, new_width, 3), dtype=np.uint8, cacheable=1)
in_buffer[:] = np.array(original_image)

resizer.register_map.src_rows = old_height
resizer.register_map.src_cols = old_width
resizer.register_map.dst_rows = new_height
resizer.register_map.dst_cols = new_width

def run_kernel():
    dma.sendchannel.transfer(in_buffer)
    dma.recvchannel.transfer(out_buffer)
    resizer.write(0x00, 0x81)
    dma.sendchannel.wait()
    dma.recvchannel.wait()

print("Warmup...", flush=True)
run_kernel()

print("Running DPU FPGA 20 runs...", flush=True)
dpu_times = []
for _ in range(20):
    t = time.time()
    run_kernel()
    _ = Image.fromarray(out_buffer)
    dpu_times.append((time.time() - t) * 1000)

print("Running ARM CPU 20 runs...", flush=True)
arm_times = []
for _ in range(20):
    t = time.time()
    _ = original_image.resize((new_width, new_height), Image.BILINEAR)
    arm_times.append((time.time() - t) * 1000)

d = np.array(dpu_times)
a = np.array(arm_times)

print()
print(f"Task: {old_width}x{old_height} -> {new_width}x{new_height} bilinear | n=20")
print("=" * 55)
print(f"{'Metric':<20} {'DPU (FPGA)':<18} {'ARM Processor'}")
print("-" * 55)
print(f"{'Mean (ms)':<20} {d.mean():<18.1f} {a.mean():.1f}")
print(f"{'Std dev (ms)':<20} {d.std():<18.1f} {a.std():.1f}")
print(f"{'Min (ms)':<20} {d.min():<18.1f} {a.min():.1f}")
print(f"{'Max (ms)':<20} {d.max():<18.1f} {a.max():.1f}")
print(f"{'FPS':<20} {1000/d.mean():<18.1f} {1000/a.mean():.1f}")
print(f"{'Speedup':<20} {a.mean()/d.mean():.2f}x vs baseline")
print("=" * 55)

del in_buffer, out_buffer

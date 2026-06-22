# KV260 Face Detection + Servo Control

Real-time face detection on the AMD Kria KV260, with a physical servo response via an Arduino Mega 2560. When a face is detected, the servo sweeps automatically. A live MJPEG stream is accessible from any browser on the local network.

---

## Hardware

| Component | Details |
|---|---|
| AMD Kria KV260 | Runs Python, OpenCV, Flask |
| Elegoo Mega 2560 | Controls the servo via serial |
| USB Webcam | Connected to KV260 |
| Servo Motor | Attached to pin 9 on the Mega |
| USB-A to USB-B cable | KV260 → Mega serial link |

---

## How It Works

1. KV260 captures webcam frames and runs OpenCV Haar Cascade face detection
2. When a face is detected, the KV260 sends an angle over USB serial to the Mega
3. The Mega moves the servo to that angle
4. A sweep (`0° → 90° → 180° → 90° → 0°`) triggers every 10 seconds while a face is present
5. A live annotated video stream is served at `http://kria.local:5000`

---

## Files

| File | Description |
|---|---|
| `kria_app.py` | Main app — Flask web UI, face detection loop, servo control |
| `servo_test.ino` | Arduino sketch for the Elegoo Mega |

---

## Setup

### Arduino (Elegoo Mega 2560)

1. Open `servo_test.ino` in the Arduino IDE
2. Upload to the Mega
3. Connect the Mega to the KV260 via USB

### KV260

Install dependencies:

```bash
pip install flask pyserial opencv-python
```

Run the main app:

```bash
python3 kria_app.py
```

Open in a browser: `http://kria.local:5000`

Flask serves the web UI and the live MJPEG stream. It runs on the KV260 and is accessible from any device on the same network — phone, laptop, etc.

---

## Serial Protocol

The KV260 sends a plain integer string (e.g. `"90"`) over `/dev/ttyACM0` at 9600 baud. The Mega reads it with `Serial.parseInt()` and moves the servo to that angle (0–180°).

---

## Notes

- The Mega needs ~4 seconds after serial connect before it accepts commands
- If the Mega enumerates as `/dev/ttyACM1`, update the port in the Python scripts
- The servo sweep is rate-limited to once every 10 seconds to avoid jitter

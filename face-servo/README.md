# Face Detection Servo Project

## What does it do?

This project uses a camera to detect faces in real time. When a face is detected, it automatically moves a servo motor. The live camera feed can be viewed from brower on phone or laptop.

Here is the basic idea:

```
Camera → KV260 board sees a face → tells Arduino → servo moves
                    ↕
             the browser
             http://192.168.68.200:5000
             [Start] [Stop] + live video
```

---

## The Hardware

### AMD Kria KV260
This is a small but powerful computer board made by AMD. It runs Linux like a regular computer, so we can write and run normal Python code on it.

It looks at the camera 15-20 times per second and figures out if there is a face in the image. When a face is detected, the KV260 sends a string (ex: "90") to the Arduino. It also runs the website that is opened on browser.

### Arduino Mega 2560 (Elegoo)
The KV260 is good at AI and running software, but it cannot directly control a servo motor. Servo motors need a precise electrical signal that has to arrive at exactly the right time, every few milliseconds. The KV260 can't guarantee that.

The Arduino waits for the KV260 to say "move to this angle" and then it moves the servo perfectly.

The two boards talk to each other over a USB cable.

### SG90 Servo Motor
A small hobby servo that can rotate to any angle between 0° and 180°. The servo motor is connected to the Arduino's 5V, GND, and digital ping 9. When a face is detected, it sweeps from one side to the other and back. 

### USB Webcam (Logitech)
Plugged into the KV260. This is what sees the faces.

---

## The Software

**On the KV260 — `kria_app.py`**
A Python program that does three things at once:
- Reads frames from the webcam and scans for faces using OpenCV (a computer vision library)
- Streams the live video to the phone's browser
- Sends a "move" command to the Arduino whenever a face is detected

**On the Arduino — `servo_test.ino`**
A program (called a "sketch") uploaded to the Arduino. It listens for angle numbers coming from the KV260 and moves the servo to that angle.

The Arduino sketch only needs to be uploaded once. After that it lives on the Arduino.

---

## How to run

### First time only — set up the Arduino
Open `servo_test.ino` in the Arduino IDE and upload it to the Elegoo Mega. This only needs to be done once.

### Every time — start the app

SSH into the KV260 and run:
```bash
ssh ubuntu@192.168.68.200
# password: amdkria

cd ~/robotics
source /home/ubuntu/vitis-env/bin/activate
nohup python -u kria_app.py > kria_app.log 2>&1 &
```

Then open the browser and go to:
```
http://192.168.68.200:5000
```

Tap **Start** and the camera will turn on. Stand about 1-2 meters away and a green box will appear around the face. Every 10 seconds that a face is visible, the servo will sweep back and forth.

Tap **Stop** to turn everything off.

---

## Things to watch out for

- **Stand 1-2 meters from the camera** — too close and it can't see the whole face
- **The Arduino takes a moment to wake up** — the app waits 4 seconds after connecting before sending any commands, so the servo may not move immediately
- **Only one program can control the servo at a time** — make sure no other scripts are running before starting the app
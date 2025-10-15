# Initial Program - Documentation

## 1. About
This project integrates external libraries for installing PiRacer, focusing on NVIDIA boards.
We use these libraries as a foundation for initial configurations, testing electronic components, and as a reference for applying reverse engineering to understand how motors and communication protocols, such as I²C, work.

## 2. Install

To access the device remotely, see this SSH connection tutorial:
- [How to Connect to a Remote Server via SSH (DigitalOcean)](https://www.digitalocean.com/community/tutorials/how-to-use-ssh-to-connect-to-a-remote-server)

Install the main dependencies with:

```bash
pip install torch jetson-utils jetracer numpy opencv-python pandas matplotlib flask pygame
```

Check the official repositories for specific installation instructions:

- [PyTorch](https://github.com/pytorch/pytorch) – Library for GPU-accelerated computing and deep learning.
- [jetson-utils](https://github.com/dusty-nv/jetson-utils) – Utilities for image and video processing optimized for Jetson.
- [jetracer](https://github.com/NVIDIA-AI-IOT/jetracer) – Framework for autonomous car control with NVIDIA Jetson.
- [pandas](https://github.com/pandas-dev/pandas) – Data structures and statistical analysis in Python.
- [matplotlib](https://github.com/matplotlib/matplotlib) – Graphical visualization and chart generation in Python.
- [flask](https://github.com/pallets/flask) – Microframework for building web applications.
- [opencv-python](https://github.com/opencv/opencv-python) – Image processing and computer vision.
- [pygame](https://github.com/pygame/pygame) – Library for game development and multimedia interfaces.



## 3. Created main.py

The `main.py` file was created as the main entry point of the project. It uses the following libraries:

- `jetracer` ([NVIDIA-AI-IOT/jetracer](https://github.com/NVIDIA-AI-IOT/jetracer)): Autonomous vehicle control.
- `pygame` ([pygame/pygame](https://github.com/pygame/pygame)): Joystick reading and control interface.
- `time`: Time control and delays.
- Other libraries may be added as needed.

## 4. Created run.py and added to crontab -e

The `run.py` file was created for project automation. For automatic execution, add to `crontab -e`:
```bash
* * * * * /usr/bin/flock -n /tmp/run.lock /path/to/your/script.sh >> /path/to/your/log.txt 2>&1
```

This line in crontab does the following:

Runs the script /path/to/your/script.sh every minute, but does not start a new execution if the previous one is still running.
All output and errors from the script are appended to /path/to/your/log.txt.

The trick is flock -n /tmp/run.lock, which creates a “lock” to prevent multiple simultaneous executions.

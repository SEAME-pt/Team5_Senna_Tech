# CARLA Simulator: Initial Setup and Real-Time Camera Visualization

## Table of Contents

1. [Starting the CARLA Server](#1-starting-the-carla-server)
2. [Connecting to CARLA via Python API](#2-connecting-to-carla-via-python-api)
3. [Selecting a World](#3-selecting-a-world)
4. [Spawning a Vehicle](#4-spawning-a-vehicle)
5. [Attaching a Camera Sensor](#5-attaching-a-camera-sensor)
6. [Capturing Sensor Data](#6-capturing-sensor-data)
7. [Displaying Frames with OpenCV](#7-displaying-frames-with-opencv)
8. [Cleaning Up](#8-cleaning-up)

---

## 1. Starting the CARLA Server

The first step in working with CARLA is **start the CARLA server**, which runs the simulation environment.

- Launch the server executable provided by CARLA.
- The server initializes a physics-based world with all required maps, assets, and traffic infrastructure.
- By default, the server listens for connections on **`localhost`** using **port `2000`**.

> Once the server is running, Python clients can connect to it to control actors, spawn vehicles, and receive sensor data.

---

## 2. Connecting to CARLA via Python API

To interact with the simulation from Python:

- Import the CARLA Python API module.
- Create a **client object** pointing to the server host (`localhost`) and default port (`2000`).

The client establishes a connection with the running server, allowing access to the simulation world and all its objects.

```python
import carla

client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
```

---

## 3. Selecting a World

Once connected:

- The client can retrieve the **current world** from the server.
- The world contains the map layout, environment settings, traffic infrastructure, and all spawned actors.

This step is essential to begin adding new vehicles or sensors to the environment.

```python
world = client.get_world()
```

---

## 4. Spawning a Vehicle

After selecting the world:

1. Access the **blueprint library**, which contains definitions for all available vehicles and sensors.
2. Select a vehicle blueprint (e.g., an Audi TT) and customize attributes such as color.
3. Choose a **spawn point** from the map's list of locations.
4. Use the world to **spawn the vehicle actor** at the chosen location.
5. Optionally, enable **autopilot** to let the vehicle navigate automatically.

```python
blueprint_library = world.get_blueprint_library()
vehicle_bp = blueprint_library.find('vehicle.audi.tt')
vehicle_bp.set_attribute('color', '255,0,0')

spawn_point = world.get_map().get_spawn_points()[0]
vehicle = world.spawn_actor(vehicle_bp, spawn_point)
vehicle.set_autopilot(True)
```

---

## 5. Attaching a Camera Sensor

To capture visual data:

1. Select a **camera blueprint** from the blueprint library.
2. Configure attributes such as **resolution** (`image_size_x`, `image_size_y`) and **field of view** (`fov`).
3. Define a **transform** that positions the camera relative to the vehicle (e.g., slightly above with a slight downward pitch).
4. Spawn the camera **attached to the vehicle**, so it moves along with it.

```python
camera_bp = blueprint_library.find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '1280')
camera_bp.set_attribute('image_size_y', '720')
camera_bp.set_attribute('fov', '90')

camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4), carla.Rotation(pitch=-15))
camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
```

---

## 6. Capturing Sensor Data

CARLA sensors **push data asynchronously** via callbacks:

- Define a **callback function** that receives sensor measurements on each new frame.
- Inside the callback:
  - Convert raw sensor data into a usable image format.
  - Extract RGB (or BGR) channels for display or processing.
  - Store the processed frame in a **queue** for safe consumption outside the callback.

```python
import queue
import numpy as np

frame_queue = queue.Queue()

def process_image(image):
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = array.reshape((image.height, image.width, 4))  # RGBA
    bgr = array[:, :, :3][:, :, ::-1]                      # Convert to BGR
    frame_queue.put(bgr)

camera.listen(process_image)
```

> This architecture ensures frames are captured continuously without blocking the simulation loop.

---

## 7. Displaying Frames with OpenCV

To visualize the camera feed in real-time:

- Initialize a loop that continuously checks the queue for new frames.
- For each available frame, display it in an **OpenCV window**.
- Use a small delay (`cv2.waitKey`) to allow GUI refresh and keyboard interaction.

```python
import cv2

while True:
    if not frame_queue.empty():
        frame = frame_queue.get()
        cv2.imshow('CARLA Camera Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

---

## 8. Cleaning Up

Proper cleanup is crucial to avoid resource leaks:

- Close all OpenCV windows.
- Destroy all actors (vehicles, cameras, sensors) spawned in the simulation.

```python
cv2.destroyAllWindows()
camera.destroy()
vehicle.destroy()
```

> Ensuring cleanup keeps the simulation environment stable for future runs.

---


By following these steps, users can establish a **fully interactive simulation environment**, allowing experimentation with autonomous driving, sensor fusion, and computer vision applications.
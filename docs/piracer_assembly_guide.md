
# 🏎️ PiRacer Assembly – Quick Guide

Based on the [PiRacer Assembly Manual by Waveshare](https://www.waveshare.com/wiki/PiRacer_Assembly_Manual)

---

## 🧰 Materials Needed  

Before starting the assembly, make sure you have all components and tools ready.  
Below is the complete list of items included in the PiRacer kit and what you’ll need to assemble it.

### 🔩 Components

![materials](docs/pictures/material.jpeg)

- Metal chassis  
- 2× DC gear motors  
- 2× Rear wheels  
- 2× Front wheels with steering knuckles  
- Servo motor  
- Servo bracket and linkage bars (short + long)  
- Expansion board (HAT)  
- Raspberry Pi (e.g., Pi 4 or Pi 5)  
- Camera module + acrylic mount + nylon screws  
- EVA vibration pads  
- Standoffs (M3×22, M3×26)  
- Screws (M3×6, M4×8, copper screws, locknuts)  
- Couplers and spacers  
- 6-pin connection cable (Pi ↔ Expansion board)  
- Battery and holder  

 

---

## 🔧 Step-by-Step Assembly

### 1. Mount the Motors

![motors](docs/pictures/motors.jpeg)

- Fasten the motors to the metal chassis using **M3×6** screws.  
- Ensure they are properly aligned and firmly secured.  

### 2. Assemble the Wheels

![wheels](docs/pictures/back_wheels.jpeg)

- Attach the couplers to the wheels and secure them with **M4×8** screws.  
- Mount the wheels onto the shafts and tighten the screws until they spin freely.  

### 3. Install the Servo and Linkage Bars

![servo](docs/pictures/servo_bars.jpeg)

- Mount the servo bracket onto the chassis.  
- Fix the servo onto the bracket and align it correctly.  
- Connect the short bar to the servo (“servo pull bar”) and the long bar to the front steering (“front pull bar”).  
- Link both to the **steering knuckles** (the front wheel connectors).  

### 4. Mount the Front Wheels

![front_wheels](docs/pictures/front_wheels.jpeg)

- Install the wheels onto the knuckles using **M4 screws** and **locknuts**.  
- Check that the wheels spin freely.  

### 5. Build the Front Structure and Pads for Protection

![EVA](docs/pictures/EVA.jpeg)

- Add the **standoffs (M3×22)** and the front wheel support.  
- Attach the **EVA pads** for vibration damping.  

### 6. Connect the Motors and Servo Wires

![HAT Connection](docs/pictures/HAT_connection.jpeg)

- Identify the connectors on the **Expansion Board (HAT)** for the **left and right motors** and the **servo**.  
- Connect each wire according to its label and **ensure correct polarity**:
  - **Brown → GND**  
  - **Red → 5V (Power)**  
  - **Yellow → Signal (PWM or control line)**  
- Verify that all wires are firmly attached and not crossing each other.  

### 7. Mount the Expansion Board (HAT)

![HAT Assemble](docs/pictures/HAT_assemble.jpeg)

- Place the expansion board onto the **M3×26 standoffs** and secure it with **copper screws**.  
- Ensure that all connectors (motors, servo, power input) are accessible and the board is firmly attached to the chassis. 

### 8. Install the Raspberry Pi

![Raspberry](docs/pictures/raspberry_assemble.jpeg)

- Mount the Raspberry Pi on top of the expansion board using screws.  
- Connect the **6-pin cable** between the Pi and the expansion board.
#### 🧠 Understanding the I²C Connection

![Raspberry](docs/pictures/raspberry_connection.jpeg)

- The **I²C (Inter-Integrated Circuit)** protocol allows the Raspberry Pi to communicate with the HAT using only **two data lines**:
  - **SDA (Data)** → Transmits and receives data.  
  - **SCL (Clock)** → Synchronizes the data transmission.  
- Through this interface, the Raspberry Pi can send control commands to the **motor drivers**, **servo controller**, and **sensor modules** on the expansion board.  
- The **I²C bus** supports multiple devices, each with a unique **address**, allowing easy expansion with components like **IMUs**, **encoders**, or **battery sensors**.  
- Ensure the cable is properly seated on both connectors (usually labeled **SDA**, **SCL**, **5V**, and **GND**) and that the Raspberry Pi’s **I²C interface is enabled**:

### 9. Final Assembly

![final](docs/pictures/final_assembly.jpeg)

- Organize all wiring neatly and install the motor cover.  
- Place the battery into its compartment and connect it (make sure it’s charged before use).  

---

## ✅ Final Checks

- All parts are secure and well aligned.  
- Wheels spin freely.  
- Servo and motors are properly connected.  
- No loose wires or short circuits.  

---

## 📚 Reference

Full assembly manual: [**Waveshare – PiRacer Assembly Manual**](https://www.waveshare.com/wiki/PiRacer_Assembly_Manual)
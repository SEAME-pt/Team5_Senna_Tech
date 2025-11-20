# 📚 Project Documentation: CAN-BUS Bridge (STM32 <-> Raspberry Pi)

## 1. System Overview
The objective of this project is to establish bidirectional communication via the **CAN (Controller Area Network)** protocol between an **STM32U585AI** microcontroller and a **Raspberry Pi 4** embedded computer.

Both devices utilize the **MCP2515** CAN controller and the **TJA1050** transceiver to interface with the physical network.

* **Protocol:** CAN 2.0B
* **Speed (Baudrate):** 500 kbps
* **Crystal Frequency (Modules):** 8 MHz
* **Reception Method (STM32):** Polling (Cyclic verification)

---

## 2. Hardware & Physical Connections

### 2.1. STM32 Side (Node A)
* **Board:** STM32 B-U585I-IOT02A (STM32U585AI Microcontroller)
* **Interface:** CN13 Connector (Arduino Standard)
* **Peripheral Used:** SPI1

**Pinout Table (STM32 -> MCP2515):**

| STM32 Pin (Name) | Header CN13 Pin | Function | Pin on MCP2515 Module | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **PE13** | D13 (Pin 6) | **SCK** | SCK | SPI Clock |
| **PE14** | D12 (Pin 5) | **MISO** | SO | Data (Slave Out) |
| **PE15** | D11 (Pin 4) | **MOSI** | SI | Data (Slave In) |
| **PE12** | D0 (Pin 3) | **CS** | CS | Chip Select (Software Controlled) |
| **3.3V** | 3.3V | **VCC** | VCC | Main Power |
| **GND** | GND | **GND** | GND | Common Ground |

>You can see the pinout layout here: [user manual](https://www.st.com/resource/en/user_manual/um2839-discovery-kit-for-iot-node-with-stm32u5-series-stmicroelectronics.pdf)

---

### 2.2. Raspberry Pi Side (Node B)
* **Board:** Raspberry Pi 4 Model B
* **Operating System:** Raspberry Pi OS (Kernel 6.x - Bookworm)
* **Peripheral Used:** SPI0

**Pinout Table (Raspberry Pi -> MCP2515):**

| RPi Pin (Physical) | GPIO (Broadcom) | Function | Pin on MCP2515 Module |
| :--- | :--- | :--- | :--- |
| **Pin 2 or 4** | - | **3.3V** | VCC |
| **Pin 6, 9...** | - | **GND** | GND |
| **Pin 23** | GPIO 11 | **SCLK** | SCK |
| **Pin 21** | GPIO 9 | **MISO** | SO |
| **Pin 19** | GPIO 10 | **MOSI** | SI |
| **Pin 24** | GPIO 8 | **CE0** | CS |
| **Pin 22** | GPIO 25 | **INT** | INT (Required for Linux Driver) |

> See all documentation [here](https://www.raspberrypi.com/documentation/)

---

### 2.3. The CAN Network (Bus)
The physical connection between the two nodes.

* **CAN High (H):** Connect H of Module A to H of Module B.
* **CAN Low (L):** Connect L of Module A to L of Module B.
* **Common GND:** Connect a common ground (between STM and RPi). (Essential for signal stability).
* **Termination:** 120 Ohm resistors installed at both ends of the bus (typically enabled via Jumper J1 on the modules).

---

## 3. Software Configuration - STM32

### 3.1. STM32CubeMX (.ioc)
1.  **SPI1:** Configured as **Full-Duplex Master**.
    * *Prescaler:* Adjusted to ensure SPI speed does not exceed 10MHz (ours is 16).
    * *CPOL:* Low.
    * *CPHA:* 1 Edge.
2.  **PE12:** Configured as **GPIO_Output**.
    * *Output Level:* High (Start inactive).
    * *User Label:* `MCP_CS`.(optional)

### 3.2. Source Code
The implementation uses the **Polling** method (checks for messages in every loop cycle).

**File: `mcp2515.h` (Configuration)** 

[mcp2515.h](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/feature/CAN/src/CAN_communication/mcp2515.h)

Defines registers and Chip Select pins.

**File: `mcp2515.c` (Driver)**

[mcp2515.c](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/feature/CAN/src/CAN_communication/mcp2515.c)

Implements SPI communication logic.

**Key points:**
- **Reset:** Sends command 0xC0
- **Bitrate:** Configures registers CNF1, CNF2, CNF3
  - For 500kbps @ 8MHz: CNF1=0x00, CNF2=0x90, CNF3=0x02
- **Normal Mode:** Writes 0x00 to CANCTRL
- **TX (Send):** Loads ID and Data into TXB0... registers and sends RTS command
- **RX (Receive):** Reads CANINTF. If bit 0 is 1, reads RXB0... registers and clears the flag

**File: `main.c` (Application)**
[main.c](https://github.com/SEAME-pt/Team5_Senna_Tech/blob/feature/CAN/src/CAN_communication/main.c)

---

## 4. Software Configuration - Raspberry Pi

### 4.1. System Configuration

1. In the /boot/firmware/config.txt file, add/verify the following lines:
```bash
dtparam=spi=on
dtoverlay=mcp2515,oscillator=8000000,spi0-1,irq-pin=25
```
oscillator: Must match the module's(MCP2515) crystal (8000000 for 8MHz).

2. Configuration Commands
```bash
# Enable SPI
sudo raspi-config nonint do_spi 0

# Configure can0 interface for 500kbps (matching STM32)
sudo ip link set can0 down
sudo ip link set can0 up type can bitrate 500000

# Test communication
candump can0
cansend can0 123#AABBCCDD

# For loopback testing
sudo ip link set can0 up type can bitrate 500000 loopback on
```

🛠️ Useful Diagnostic Commands
```bash
# Check SPI
ls -la /dev/spi*
lsmod | grep spi

# Check CAN
ip -details link show can0
dmesg | grep -i mcp2515

# To verify status
ifconfig can0
ip -s link show can0
```
Or for a complete diagnosis
```bash
echo "COMPLETE DIAGNOSIS OF CAN"
echo "================================"

# 1. Check interface
echo "1. CAN interface status:"
ip -details link show can0

# 2. Check statistics
echo "2. CAN statistics:"
cat /proc/net/can/stats

# 3. Direct communication test
echo "3. Raw communication test:"
timeout 3s candump can0 &
sleep 1
cansend can0 100#01
sleep 2
sudo pkill candump

# 4. Checking for errors
echo "4. Checking for errors:"
cat /sys/class/net/can0/statistics/ 2>/dev/null

echo "================================"
```
---

## 5. Testing & Validation

1. Physical Loopback Test
To test Raspberry Pi hardware only:
Short-circuit MOSI and MISO pins on the RPi.
Run Python spidev script (with the kernel driver temporarily disabled).
```bash
# Single terminal
timeout 10s candump can0 &
cansend can0 123#AABBCCDDEEFF
```
Expected Result:
```bash
can0  123   [6]  AA BB CC DD EE FF
can0  123   [6]  AA BB CC DD EE FF  # Loopback
```
2. Bidirectional Communication Validation
Test A: STM32 Sending to RPi
STM32 runs the periodic send code.
Raspberry Pi executes: candump can0
Result: Data appears in the RPi terminal (can0 123 [2] ...).

Test B: RPi Commanding STM32
STM32 runs the reception code (polling).
Raspberry Pi executes: cansend can0 123#01
Result: On STM32, in our case via the swv console, receives the message.

The two tests can be done simultaneously, as expected. Both can receive and send messages.

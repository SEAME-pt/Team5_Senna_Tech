
# 📚 Project Documentation: CAN-BUS Bridge (STM32 <-> Raspberry Pi)

## 1. System Overview
The objective of this project is to establish bidirectional communication via the **CAN (Controller Area Network)** protocol between an **STM32U585AI** microcontroller and a **Raspberry Pi 5 (with AGL OS)** embedded computer. Additionally, the system monitors the rotation speed of a motor using an LM393 sensor.

Both devices utilize the **MCP2515** CAN controller and the **TJA1050** transceiver to interface with the physical network.

* **Protocol:** CAN 2.0B
* **Speed (Baudrate):** 500 kbps
* **Crystal Frequency (Modules):** 8 MHz
* **Reception Method (STM32):** **Interrupt (EXTI)** - Event-driven reception.

### 🧠 Architecture Change: Polling vs. Interrupt
The project has migrated from a **Polling** architecture to an **Interrupt** architecture to improve efficiency.

| Feature | Old Method (Polling) | New Method (Interrupt) |
| :--- | :--- | :--- |
| **Concept** | The CPU constantly asks: "Is there data?" | The CPU waits. Hardware notifies: "Data arrived!" |
| **Analogy** | Checking the mailbox every 5 minutes. | Installing a doorbell. |
| **CPU Usage** | High (wasted cycles checking empty buffer). | Low (CPU sleeps or processes other tasks). |
| **Latency** | Variable (depends on loop speed). | Immediate (microsecond reaction). |
| **Hardware** | Only SPI pins required. | **Requires extra INT pin connection.** |

---

## 2. Hardware & Physical Connections

### 2.1. STM32 Side (Node A)
* **Board:** STM32 B-U585I-IOT02A (STM32U585AI Microcontroller)
* **Interface:** CN13 Connector (Arduino Standard)
* **Peripherals Used:**
    * **SPI1:** Communication with MCP2515.
    * **EXTI0 (PB0):** Speed Sensor (LM393).
    * **EXTI7:** CAN Interrupt (MCP2515).

**Pinout Table (STM32 -> MCP2515):**

| STM32 Pin (Name) | Function | Pin on MCP2515 Module | Notes |
| :--- | :--- | :--- | :--- |
| **PE13** | **SCK** | SCK | SPI Clock |
| **PE14** | **MISO** | SO | Data (Slave Out) |
| **PE15** | **MOSI** | SI | Data (Slave In) |
| **PE12** | **CS** | CS | Chip Select |
| **[Your_PIN]** | **EXTI7**| **INT** | **Interrupt Pin (Active Low)** |
| **3.3V** | **VCC** | VCC | Main Power |
| **GND** | **GND** | GND | Common Ground |


**Pinout Table (STM32 -> LM393 Speed Sensor):**

| STM32 Pin | Function | Sensor Pin | Notes |
| :--- | :--- | :--- | :--- |
| **PB0 (D0)** | **EXTI0** | **D0** | Digital Output (Pulses) |
| **3.3V** | **VCC** | VCC | |
| **GND** | **GND** | GND | |

---

### 2.2. Raspberry Pi Side (Node B)
* **Board:** Raspberry Pi 5 Model B
* **Operating System:** Automotive Grade Linux (AGL) (Trout version)
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

---

### 2.3. The CAN Network (Bus)
The physical connection between the two nodes.

* **CAN High (H):** Connect H of Module A to H of Module B.
* **CAN Low (L):** Connect L of Module A to L of Module B.
* **Common GND:** Connect a common ground (between STM and RPi). (Essential for signal stability).
* **Termination:** 120 Ohm resistors installed at both ends of the bus.

---

## 3. Data Protocol Specification

This section defines how the STM32 formats the data sent to the Raspberry Pi.

* **CAN ID:** `0x123` (Standard Frame)
* **DLC (Data Length Code):** 2 Bytes
* **Transmission Rate:** ~10 Hz (Every 100ms)
* **Byte Order:** **Big Endian** (Most Significant Byte First)

| Byte Index | Content | Formula | Example |
| :--- | :--- | :--- | :--- |
| **Data[0]** | Pulse Count (High Byte) | `(pulse_count >> 8) & 0xFF` | Count 300 (0x012C) -> **0x01** |
| **Data[1]** | Pulse Count (Low Byte) | `(pulse_count) & 0xFF` | Count 300 (0x012C) -> **0x2C** |

> **Note 1:** To reconstruct the integer value: `uint16_t pulses = (Data[0] << 8) | Data[1];`

> **Note 2:** Message abstraction protocols have not yet been applied.

---

## 4. Software Configuration - STM32 (Updated)

The software architecture has moved from a Polling approach to a fully **Interrupt-Driven** approach.

### 4.1. STM32CubeMX Configuration (.ioc)
1.  **SPI1:** Configured as **Full-Duplex Master** (Prescaler adjusted for <10MHz).
2.  **PB0 (Sensor):** Configured as `GPIO_EXTI0` (Rising/Falling edge).
    * *NVIC:* EXTI Line0 Interrupt Enabled (Priority 0 - Highest).
3.  **[Pin EXTI7] (CAN):** Configured as `GPIO_EXTI7` (Falling Edge - since MCP2515 INT is Active Low).
    * *NVIC:* EXTI Line7 Interrupt Enabled (Priority 1).

### 4.2. Source Code Logic

#### The "Direct ISR" Approach
To handle high-speed pulses from the sensor and fix Vector Table offset issues on STM32U5, a direct approach was used in `stm32u5xx_it.c`.

**File: `stm32u5xx_it.c`**
* **`EXTI0_IRQHandler` (Sensor):**
    * Clears the interrupt flag directly via registers (`EXTI->RPR1`).
    * Increments the `pulse_count` variable immediately.
    * Uses `__attribute__((used))` and `extern "C"` to ensure the Linker correctly maps the function.

* **`EXTI7_IRQHandler` (CAN):**
    * Calls the standard `HAL_GPIO_EXTI_IRQHandler`.

**File: `main.c`**
* **Initialization:**
    * `SCB->VTOR` is explicitly set (`0x08000000`) to fix Vector Table offset issues.
    * `MX_OCTOSPIx_Init` functions are **disabled** to prevent pin conflict on PB0.
    * `__set_PRIMASK(0)` ensures global interrupts are enabled.
    * MCP2515 is configured with `MCP_CANINTE = 0x01` (RX Buffer Interrupt Enabled).

* **Main Loop (`while(1)`):**
    1.  **Speed Calculation:** Every 100ms, calculates RPM/Velocity based on the `pulse_count` delta.
    2.  **CAN TX:** Sends the current pulse count to the bus.
    3.  **CAN RX:** Checks `flag_mensagem_recebida`. If true, reads the CAN frame via SPI and prints the data.

### 4.3. Key Diagrams

**Flow: CAN Message Reception (Interrupt Mode)**
```bash
    participant BUS as CAN Bus
    participant MCP as MCP2515
    participant INT as STM32_INT_Pin
    participant CPU as STM32_Main
    
    BUS->>MCP: New Message Arrives
    MCP->>INT: Pulls Pin LOW (Trigger)
    INT->>CPU: Fire EXTI7 ISR
    CPU->>CPU: Set flag_received = 1
    CPU->>MCP: SPI Read Message
    MCP->>BUS: Message Cleared
    INT->>MCP: Pin goes HIGH
```

## 5. Raspberry Pi Configuration (Software)
5.1. System Configuration
1. In the /boot/firmware/config.txt file:

```bash
dtparam=spi=on
dtoverlay=mcp2515,oscillator=8000000,spi0-1,irq-pin=25
```
2. Configuration Commands
```bash
# Enable SPI
sudo raspi-config nonint do_spi 0

# Configure can0 interface for 500kbps (matching STM32)
sudo ip link set can0 down
sudo ip link set can0 up type can bitrate 500000

#Useful Diagnostic Commands
ip -details link show can0
dmesg | grep -i mcp2515
```

## 6. Testing & Validation
1. Speed Sensor Test
Rotate the encoder disc. The STM32 console should print (SWV) the speed data.

Expected Output (Serial Console):
```bash
pulse counting: 150
TX CAN OK: pulse_count=150
```

2. CAN Bidirectional Test
STM32 Sending: The STM32 automatically sends a frame ID 0x123 every 100ms containing the pulse count.

On Raspberry Pi:
```bash
candump can0
# Output: can0  123   [2]  00 96  (Representing 150 pulses)
```
STM32 Receiving: Send a command from the Raspberry Pi.

On Raspberry Pi:
```bash
cansend can0 123#AABBCC
```
On STM32 Console:

```bash
RX CAN ID=0x123 DLC=3 Data=AA BB CC
```


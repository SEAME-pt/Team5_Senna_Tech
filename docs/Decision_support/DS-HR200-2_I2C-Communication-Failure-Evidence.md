# Evidence for HARA-200: I²C Communication Failure Modes (NACK, Timeout)

**ID:** DS-HR200-2  
**Date:** 2026-01-08  
**Author:** Gemini  
**Reviewer:** [Pending Human Review]  
**Relates to:** HARA-200, Hazard H1-200 (I²C Communication Failure)  

---

## 1. Decision

Hazard H1-200, "I²C Communication Failure (e.g., NACK, Timeout)", is a valid and well-documented failure mode for the I²C protocol. The implementation of an I²C-based speedometer on the STM32U5 must consider and mitigate these failure conditions.

## 2. Justification

The I²C protocol inherently includes mechanisms that can lead to NACK (Not Acknowledged) conditions and is susceptible to scenarios that can result in communication timeouts [1, 7]. These are recognized error states that require robust handling.

### 2.1 NACK Conditions (Not Acknowledged)

A NACK occurs when the SDA (Serial Data) line remains high during the ninth clock pulse [1, 2]. Common causes and mitigations for unexpected NACKs include:

*   **No Slave at Address:** The master attempts to communicate with a slave address for which no device exists or responds [1, 4].
    *   **Mitigation:** The I²C driver should detect this NACK, issue a STOP condition to release the bus, and report a "device not found" error to the application layer. The application should not retry indefinitely.

*   **Slave Busy:** The addressed slave is temporarily unable to process the request due to internal operations [3, 4].
    *   **Mitigation:** The driver can issue a STOP condition and retry the transaction after a short, predefined delay. A limit on the number of retries should be implemented to prevent an infinite loop.

*   **Invalid Data/Command:** The slave receives data or a command it does not understand [4].
    *   **Mitigation:** This indicates a software logic error in the master. The driver should report a critical error to the application layer. The event should be logged for debugging, and the system should enter a safe state as this is an unexpected condition.

### 2.2 Timeout Conditions

Timeouts signify that the I²C bus remains in an unexpected state for an excessively long duration. Key scenarios and mitigations include:

*   **SCL Stuck Low (Clock Stretching Timeout):** A slave device holds the SCL (Serial Clock) line low indefinitely [1, 6, 7].
    *   **Mitigation:** Utilize the microcontroller's hardware timeout feature (if available) to detect this. Upon detection, the I²C peripheral should be reset. If the bus remains stuck, a higher-level system reset or power-cycling of the sensor may be required.

*   **Event Timeout:** A general timeout mechanism that triggers if the time between any I²C bus events exceeds a predefined limit, indicating a bus hang [7].
    *   **Mitigation:** This can be detected by hardware or a software watchdog. The recovery procedure is similar to a "Stuck Low" condition: attempt to reset the I²C peripheral and, if that fails, escalate to a system-level recovery action.

## 3. Test Environment Suggestions for Failure Provocation

To verify the driver's robustness and the system's response to these failures, the following test setups can be implemented.

### 3.1 Provoking NACK Conditions

*   **No Slave at Address:**
    *   **Method:** In software, configure the master to attempt communication with a known-unused I²C address on the bus.
    *   **Expected Result:** The driver should immediately detect a NACK and report a "device not found" error without retrying.

*   **Slave Busy:**
    *   **Method:** This is difficult to reproduce reliably with a real sensor. A more effective method is to use a second microcontroller programmed to act as an I²C slave. This "test slave" can be programmed to randomly or deterministically ignore a master request and return a NACK, simulating a busy condition.
    *   **Expected Result:** The master driver should execute its retry logic (e.g., wait and try again, up to a limit) and eventually report a communication failure if the "test slave" remains unresponsive.

*   **Invalid Data/Command:**
    *   **Method:** This is a master-side software logic test. Modify the master's code to intentionally send a command or register address that is known to be invalid for the target speedometer sensor.
    *   **Expected Result:** The sensor should return a NACK, and the master driver should report a critical error, leading to a safe state.

### 3.2 Provoking Timeout Conditions

*   **SCL Stuck Low (Clock Stretching Timeout):**
    *   **Method:** Use a "test slave" microcontroller as described above. Program the test slave to pull the SCL line low for a duration longer than the master's configured hardware/software timeout.
    *   **Alternative (Hardware):** In a controlled test environment, manually short the SCL line to ground via a push-button or a jumper wire. (Use with caution to avoid damaging components).
    *   **Expected Result:** The master's I²C timeout mechanism should trigger, and the system should initiate its bus recovery protocol (e.g., reset the I²C peripheral).

*   **Bus Hang / Event Timeout:**
    *   **Method:** This can be simulated by having a test slave start a transaction but never complete it (e.g., never releasing SDA after pulling it low). This is more advanced and best simulated with a dedicated I²C testing tool or a programmable test slave.
    *   **Expected Result:** The master's event timeout or software watchdog should trigger, leading to a bus reset and recovery attempt.

## 4. Assumptions
*   The I²C driver implemented on the STM32U5 will include mechanisms to detect and react to NACK conditions and timeouts.
*   The system's control logic will be designed to handle communication failures reported by the I²C driver.

## 5. References
[1] **Memfault Blog:** I2C: A (Not So) Trivial Protocol ([link](https://memfault.com/blog/i2c-trivial-protocol/))  
[2] **Stack Exchange:** What are the primary failure modes of I2C? ([link](https://electronics.stackexchange.com/questions/56910/what-are-the-primary-failure-modes-of-i2c))  
[3] **Texas Instruments:** I2C BUS PULLUP RESISTOR CALCULATION ([link](https://www.ti.com/lit/an/slva689/slva689.pdf))  
[4] **Stack Overflow:** I2C Master behaviour upon Slave NACK ([link](https://stackoverflow.com/questions/2984102/i2c-master-behaviour-upon-slave-nack))  
[6] **Texas Instruments:** MSP430™ I2C Bus-Stuck-Low Timeout Feature ([link](https://www.ti.com/lit/an/slaa736/slaa736.pdf))  
[7] **NXP:** UM10204, I2C-bus specification and user manual (Example of official protocol specification)  
[11] **STMicroelectronics:** AN4471, I2C bus: a simple guide to understanding and debugging ([link](https://www.st.com/resource/en/application_note/an4471-i2c-bus-a-simple-guide-to-understanding-and-debugging-stmicroelectronics.pdf))  

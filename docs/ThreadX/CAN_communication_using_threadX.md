# CAN Communication Using ThreadX and MCP2515

## 1. Overview

This module implements a ThreadX task (thread) responsible for:

* Initializing the external CAN controller MCP2515 via SPI

* Periodically transmitting CAN frames containing sensor pulse count

* Receiving CAN messages from the bus

* Managing all of this using ThreadX cooperative multitasking, avoiding blocking delays and ensuring system responsiveness

The communication is handled through the MCP2515, a standalone CAN controller commonly used when the microcontroller lacks a native CAN peripheral.

## 2. Thread Structure in ThreadX

The thread is created inside App_ThreadX_Init():
```
tx_thread_create(&sensor_thread,
                 "Sensor Thread",
                 sensor_thread_entry,
                 0,
                 sensor_thread_stack,
                 sizeof(sensor_thread_stack),
                 0,
                 0,
                 TX_NO_TIME_SLICE,
                 TX_AUTO_START);
```

#### Important parameters:

* sensor_thread_entry → Function executed by the thread

* Priority = 0 → Highest priority (may be adjusted later)

* TX_AUTO_START → Thread starts automatically when the kernel runs

## 3. ThreadX Kernel Initialization

The kernel is started with:

```
tx_kernel_enter();
```

From this point forward, ThreadX manages all scheduling, timing, and thread switching.

## 4. MCP2515 Initialization Inside the Thread

The entire CAN setup occurs inside the thread, not in main, because:

* It ensures proper synchronization

* Avoids initialization before ThreadX is running

* Allows error-handling and reconfiguration inside the task

## 5. Thread Loop (ThreadX)

The thread enters an infinite loop that performs:

#### 1. Periodic CAN Transmission (~100 ms)

Instead of HAL_Delay, the code checks elapsed time using:
```
if (tx_time_get() - last_print > 100)
```
This avoids blocking delays.

The CAN frame is prepared and sent via:
```
MCP2515_SendMessage(&frame_envio);
```

#### 2. CAN Reception

The thread checks whether the MCP2515 has new data:
```
if (MCP2515_ReceiveMessage(&rxFrame) == HAL_OK)
```

The MCP2515 handles buffering and interrupts internally; the thread simply fetches pending messages.

#### 3. Yield CPU to ThreadX

At the end of each loop cycle:
```
tx_thread_sleep(10);
```

This is essential because it:

* allows other threads to run

* keeps the system responsive

* reduces CPU load

* ensures deterministic timing

## 6. CAN Communication Strategy with ThreadX
### Dedicated communication thread

This task is responsible for:

* MCP2515 initialization

* periodic CAN transmission

* continuous CAN reception

This isolates CAN logic and avoids conflicts.

### Avoiding blocking delays

ThreadX replaces HAL_Delay() with:

* tx_thread_sleep()

* time checks using tx_time_get()

This ensures real-time operation.

## 7. Communication Flow Under ThreadX
### Thread starts

* MCP2515 initialized

* Thread enters infinite loop

* Every 100 ms → CAN TX

* Each cycle → check for CAN RX

* tx_thread_sleep(10)

* CPU released to the RTOS

## 8. Benefits of Using ThreadX for CAN Communication

| ThreadX Feature            | Benefit                                      |
|----------------------------|-----------------------------------------------|
| **Preemptive multitasking** | Ensures TX/RX operation without blocking the system |
| **Dedicated thread**        | Clean organization of communication logic    |
| **tx_thread_sleep()**       | Cooperative behavior and low power           |
| **tx_time_get()**           | Non-blocking time handling                   |
| **Deterministic operation** | Very important for CAN timing                |

## 9. Conclusion

This implementation leverages:

* ThreadX RTOS

* MCP2515 CAN controller

* SPI communication

* Periodic and responsive CAN handling

The dedicated thread ensures the CAN communication is:

* stable

* non-blocking

* synchronized

* scalable

Future improvements might include:

* interrupt-driven RX using semaphores

* priority tuning

* separating TX and RX tasks

* adding message queues for CAN processing



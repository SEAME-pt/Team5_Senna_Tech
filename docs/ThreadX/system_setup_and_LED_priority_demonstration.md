
# ThreadX System Setup and LED Priority Demonstration

## 1. System Setup (ThreadX + SysTick + MCU Configuration)

### 1.1 Enable ThreadX in STM32CubeMX

- Open STM32CubeMX.

- Go to Middleware → ThreadX.

- Enable ThreadX.

- Keep default memory configuration unless you need custom pools.

### 1.2 Verify ThreadX Integration

After code generation, confirm that:

In main.c:
```
MX_ThreadX_Init();
```
In app_threadx.c:

- App_ThreadX_Init() exists (thread creation section)

- MX_ThreadX_Init() calls tx_kernel_enter()

This ensures that:

- The RTOS kernel boots properly

- Threads can be created and scheduled

## 2. Objective

Demonstrate ThreadX preemptive scheduling using two LEDs with different priorities.

## 3. Dependencies

- ThreadX properly installed and initialized (Section 1)

- GPIO pins configured for:

    - LED_RED

    - LED_GREEN

- CubeMX-generated project

- Working HAL GPIO driver

## 4. Implementation Overview

Two threads are created:

| Thread            | LED   | Priority             | Behavior                |
|-------------------|-------|-----------------------|--------------------------|
| led_thread        | Red   | 5 (higher priority)   | Blinks with heavy workload |
| led_thread_green  | Green | 10 (lower priority)   | Blinks with light workload |

### ThreadX rule:
 Lower number = higher priority

Both use:
```
tx_thread_sleep(100);
```
But the higher-priority thread always resumes first.

## 5. Code — Thread Creation (ThreadX Setup Inside the App)
Inside ```App_ThreadX_Init()```:

```
tx_thread_create(&led_thread,
                 "LED Blink Thread",
                 led_thread_entry,
                 0,
                 led_thread_stack,
                 sizeof(led_thread_stack),
                 5,        // higher priority
                 5,
                 TX_NO_TIME_SLICE,
                 TX_AUTO_START);

tx_thread_create(&led_thread_green,
                 "LED Green Thread",
                 led_thread_green_entry,
                 0,
                 led_thread_green_stack,
                 sizeof(led_thread_green_stack),
                 10,       // lower priority
                 10,
                 TX_NO_TIME_SLICE,
                 TX_AUTO_START);
```

## 6. Code — Thread Logic (LED Priority Demo)
### Red LED Thread (High Priority)

```
void led_thread_entry(ULONG thread_input)
{
    while (1)
    {
        HAL_GPIO_TogglePin(LED_RED_GPIO_Port, LED_RED_Pin);

        for (volatile int i = 0; i < 500000; i++);

        tx_thread_sleep(100);
    }
}
```
### Green LED Thread (Low Priority)

```
void led_thread_green_entry(ULONG thread_input)
{
    while (1)
    {
        HAL_GPIO_TogglePin(LED_GREEN_GPIO_Port, LED_GREEN_Pin);

        for (volatile int i = 0; i < 500000; i++);

        tx_thread_sleep(100);
    }
}
```

## 7. Expected Behavior (Visual Scheduling Test)
✔ Both threads sleep for 100 ticks

✔ Both wake up at the same time

✔ ThreadX does NOT run them simultaneously

✔ ThreadX selects the higher-priority one first

✔ The low-priority thread is delayed

### Result:

- The red LED always toggles first

- The green LED toggles later, showing scheduling delay

- This visually confirms:

    - ThreadX priority scheduling

    - Kernel preemption is active

## 8. Acceptance Criteria

After following this document:
- ThreadX boot sequence is correct
- Threads are created and scheduled
- Higher-priority thread preempts lower-priority thread
- LED blinking demonstrates deterministic RTOS behavior
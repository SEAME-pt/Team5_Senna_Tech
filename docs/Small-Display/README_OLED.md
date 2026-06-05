# OLED (SSD1305) — Quick Summary

Short description
- Simple driver for the SSD1305 OLED used in this project. Resolution: 128x32 pixels (4 pages), RAM buffer.

Hardware
- Interface: SPI (uses `hspi3`).
- Pins used in the current code: CS -> PG12, DC -> PC12, RST -> PB13.

Features
- Buffer: `SSD1305_BUF_SIZE` = 128 * 4.
- Main operations: initialize, clear, draw pixels/lines/ellipses, update display.
- Built-in designs: eyes (cute, half-closed, closed, happy) and sleep face.

Main API (functions)
- `ssd1305_init()` — initialize the display (GPIOs, reset, SSD1305 setup).
- `ssd1305_clear()` / `ssd1305_fill(value)` — clear or fill the buffer.
- `ssd1305_update()` — send buffer to the display.
- `ssd1305_draw_pixel(x,y,color)` — set/clear a pixel in the buffer.
- `ssd1305_draw_line(...)`, `ssd1305_fill_ellipse(...)` — basic drawing routines.
- `ssd1305_draw_cute_eyes()`, `ssd1305_draw_happy_eyes(frame)`, etc. — animated designs used by the `oled` thread.

Quick usage example
```c
    ssd1305_init();
    ssd1305_clear();
    ssd1305_draw_pixel(10, 5, 1);
    ssd1305_update();
```

Integration notes
- The driver depends on HAL (`HAL_SPI_Transmit`, `HAL_GPIO_WritePin`) and ThreadX (`tx_thread_sleep`).
- The variable `hspi3` is declared `extern` in `ssd1305.h`.
- The project contains `oled_thread_entry()` which controls animations based on ultrasonic and ambient light sensors.

Customization
- To change pins, edit the `HAL_GPIO_WritePin` calls in `ssd1305.c` or centralize pins using defines in the header.
- Adjust frame delays and durations by modifying `tx_thread_sleep()` calls in the animation thread.

Common issues
- Ensure SPI and GPIO are initialized before calling `ssd1305_init()`.
- If the display stays dark, check CS, DC and RST wiring and signal levels.

Referenced files
- `src/threadx/SennaTech/Core/Inc/display/ssd1305.h`
- `src/threadx/SennaTech/Core/Src/display/ssd1305.c`
- `src/threadx/SennaTech/Core/Src/display/oled.c`

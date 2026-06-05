# Ambient Light Sensor — Quick Summary

Description
- Simple driver for the ambient light sensor used in this project. Reads raw values over I2C and publishes luminosity data to `g_ambient_data_queue`.

Hardware / Interface
- Bus: I2C (uses `hi2c2`).
- Default address: `AMBIENT_LIGHT_DEFAULT_ADDR`.
- Registers used: `AMBIENT_LIGHT_REG_ALS_CONF` (configuration), `AMBIENT_LIGHT_REG_ALS` (raw reading).

Functionality
- `AmbientLight_Init(hi2c, addr)` — initialize the sensor by writing the default configuration.
- `AmbientLight_ReadRaw(hi2c, addr, &raw)` — read 16-bit raw sensor value.
- `AmbientLight_ReadLux(hi2c, addr, &lux)` — reads raw value and converts to `float` (current implementation returns raw as float).
- `ambient_thread_entry()` — thread that periodically reads the sensor, publishes `t_ambient_data` to `g_ambient_data_queue`, and logs via `uart_send`.

Project dependencies
- Uses HAL I2C: `HAL_I2C_Mem_Write`, `HAL_I2C_Mem_Read`.
- Protected by mutex: `g_i2c2_mutex` to avoid concurrent access to the I2C bus.
- Uses ThreadX APIs: `tx_thread_sleep`, `tx_queue_send`, `tx_queue_flush`.

Usage example
```c
    uint16_t raw;
    float lux;

    AmbientLight_Init(&hi2c2, AMBIENT_LIGHT_DEFAULT_ADDR);
    if (AmbientLight_ReadRaw(&hi2c2, AMBIENT_LIGHT_DEFAULT_ADDR, &raw) == TX_SUCCESS)
    {
        AmbientLight_ReadLux(&hi2c2, AMBIENT_LIGHT_DEFAULT_ADDR, &lux);
        // use lux
    }
```

Notes and common issues
- Initialize I2C (`hi2c2`) and the `g_i2c2_mutex` before using the driver.
- If reads fail, check wiring, I2C address, and whether another master is using the bus.
- Conversion to lux is currently a 1:1 mapping from raw to float; consult the sensor datasheet to implement proper scaling if required.

Relevant files
- `src/threadx/SennaTech/Core/Src/sensor/ambient_light.c`
- `src/threadx/SennaTech/Core/Inc/sensor/ambient_light.h`

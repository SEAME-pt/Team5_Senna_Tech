# Reading battery status with the INA219 sensor

## Summary
- [Introduction](#introduction)
- [Main Functions](#main-functions)
- [Getting battery percentage](#getting-battery-percentage)


## Introduction

The INA219 is a power monitoring sensor that measures:

- Bus Voltage — the voltage present in the system.
- Shunt Voltage — the voltage drop across a shunt resistor (used to calculate current).
- Current — indirectly measured based on the voltage drop across the shunt.
- Power — the product of voltage and current.

In the Piracer, the INA219 is used to monitor the battery status, allowing you to know the charge level, instantaneous consumption, and the power delivered to the system.


## 🔧 Main Functions

#### 🟩 Reading the Bus Voltage

```cpp
float voltage = ina.getBusVoltage(); // Reads the REG_BUSVOLTAGE register from the INA219.
```

Returns the system voltage in volts (V).

The conversion (rawBusVoltage >> 3) * 0.004 applies the 4 mV/bit scaling factor.

📊 Example Output:

```bash 
Bus Voltage: 12.48 V
```

#### 🟨 Reading the Shunt Voltage

```cpp
float shunt = ina.getShuntVoltage();
```

Reads the REG_SHUNTVOLTAGE register.

Returns the voltage across the shunt resistor in volts (V).

Each bit represents 10 µV, hence the scaling factor 0.00001.

📊 Example Output:

```bash
Shunt Voltage: 0.025 V
```


#### 🟥 Reading the Current
```cpp
float current = ina.getCurrent();
```

Reads the REG_CURRENT register.

Returns the current in amperes (A).

The raw reading (rawCurrent) is multiplied by currentLSB, which is defined during calibration.

📊 Example Output:

```bash
Current: 1.75 A
```
#### 🟦 Reading the Power

```cpp
float power = ina.getPower();
```

Reads the REG_POWER register.

Returns the power in watts (W).

The raw value (rawPower) is multiplied by powerLSB.

📊 Example Output:

```bash
Power: 21.8 W
```

#### 🔋 Monitoring Battery Status

To monitor the Piracer’s battery status, you can combine the readings:

```cpp
float voltage = ina.getBusVoltage();
float current = ina.getCurrent();
float power   = ina.getPower();

printf("Battery Voltage: %.2f V\n", voltage);
printf("Battery Current: %.2f A\n", current);
printf("Battery Power: %.2f W\n", power);
```

## Getting battery percentage

# in progress
# Unit Test Documentation — `vehicleData` Class

## Overview

This document describes the unit tests implemented for the `vehicleData` class, part of the `car_cluster` Qt project.  

The tests use:

- **Google Test (gtest)** — for assertions and test structure.
- **QSignalSpy (QtTest)** — to monitor Qt signals (`Q_PROPERTY`).

The goal of the tests is to validate:

1. Correct initialization of the structure.
2. Behavior of properties (`speed`, `battery`, `temperature`, `isCharging`).
3. Correct emission of Qt signals.
4. Boundary values and input validation.

---

## Test Structure

### Test Fixture

```cpp
class vehicleTest : public testing::Test {
public: 
    vehicleData *car;
    
    vehicleTest() { car = vehicleData::instance(); }

    void SetUp() override {
        car->setSpeed(4);
        car->setBattery(100); 
        car->setTemperature(50); 
        car->setCharging(false);
    }
};
```
- Each test inherits from ``vehicleTest``.

- ``SetUp()`` initializes the ``vehicleData`` object with default values before each test.

## 1. Initialization Test

### Test: StructInitialization
```cpp
EXPECT_EQ(car->getSpeed(), 4);
EXPECT_EQ(car->getBattery(), 100);
EXPECT_EQ(car->getTemperature(), 50);
EXPECT_EQ(car->getIsCharging(), false);
```

- Ensures that getters return the expected values after ``SetUp()`` initialization.

## 2. ``speed`` tests
### a) Test: NegativeSpeedInput
```cpp
EXPECT_THROW(car->setSpeed(-4), std::invalid_argument);
```

- Verifies that negative values are not accepted.

### b) Test: SpeedChanging
```cpp
car->setSpeed(10);
EXPECT_EQ(car->getSpeed(), 10);
```

- Confirms that the setter correctly updates the value.

### c) Test: SpeedBoundaries
```cpp
car->setSpeed(0);
EXPECT_EQ(car->getSpeed(), 0);
car->setSpeed(100);
EXPECT_EQ(car->getSpeed(), 100);
```
- Tests the defined speed limits.

## 3. ``battery`` tests
### a) Test: BatteryChanging
```cpp
car->setBattery(70);
EXPECT_EQ(car->getBattery(), 70);
```
### b) Test: OutOfRangeBatteryInputs
```cpp
EXPECT_THROW(car->setBattery(-3), std::out_of_range);
EXPECT_THROW(car->setBattery(101), std::out_of_range);
```

- Verifies that out of range inputs are not excepted and the setter throws an **exception** for this cases

### c) Test: BatteryBoundaries
```cpp
car->setBattery(0);
EXPECT_EQ(car->getBattery(), 0);
car->setBattery(100);
EXPECT_EQ(car->getBattery(), 100);

```
### d) Test: DischargingTest
```cpp
for (int i = 100; i >= 0; i--)
    car->setBattery(i);
EXPECT_EQ(car->getBattery(), 0);

```

## 4. ``temperature`` Tests
### a) Test: TemperatureChanging
```cpp
car->setTemperature(40);
EXPECT_EQ(car->getTemperature(), 40);
```
### b) Test: OutOfRangeTemperatureInputs
```cpp
EXPECT_THROW(car->setTemperature(-2), std::out_of_range);
EXPECT_THROW(car->setTemperature(127), std::out_of_range);
```
### c) Test: TemperatureBoundaries
```cpp
car->setTemperature(0);
EXPECT_EQ(car->getTemperature(), 0);
car->setTemperature(80);
EXPECT_EQ(car->getTemperature(), 80);
```
## 5. ``isCharging`` tests

### a) Test: IsChargingTest
```cpp
EXPECT_EQ(car->getIsCharging(), false);
car->setCharging(true);
EXPECT_EQ(car->getIsCharging(), true);
```
## 6. Qt Signal tests
### a) speedChanged
```cpp
QSignalSpy spy(car, &vehicleData::speedChanged);
car->setSpeed(20);
EXPECT_EQ(spy.count(), 1);
```

- Confirms the signal is emitted only when the value changes.

### b) batteryChanged
```cpp
QSignalSpy spy(car, &vehicleData::batteryChanged);
car->setBattery(53);
EXPECT_EQ(spy.count(), 1);
```
### c) temperatureChanged
```cpp
QSignalSpy spy(car, &vehicleData::temperatureChanged);
car->setTemperature(53);
EXPECT_EQ(spy.count(), 1);
```
### d) chargingChanged
```cpp
QSignalSpy spy(car, &vehicleData::chargingChanged);
car->setCharging(true);
EXPECT_EQ(spy.count(), 1);
```

- Additional tests ensure that signals are not emitted when the value **does not** change.

## Running the Tests

### Build and Run using CMake

1. Create a build directory and navigate into it:

```bash
mkdir -p build && cd build
```
2. Configure the project with CMake:
```bash
cmake .. -DCMAKE_PREFIX_PATH="/path/to/Qt" 
```
3. Build the test executable:
```bash
make
```
4. Run the tests:
```bash
./test_car_cluster
```
### Generate XML report
```bash
./test_car_cluster --gtest_output=xml:report.xml
```

### Convert XML to HTML
  To visualize the test results in a browser, you can convert the Google Test XML report to HTML using `junit2html`.
#### Prerequisites

- **Python 3** must be installed on your system.
- Install `junit2html` via pip:

```bash
pip install --user junit2html
```

Run the command to generate an HTML report:
```bash
junit2html report.xml report.html
```

The HTML file will display:

- Which tests passed/failed

- Error messages and stack traces

- Duration of each test

- Test suite hierarchy  
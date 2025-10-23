#pragma once

#ifndef __ADAFRUIT_INA219_HPP__
#define __ADAFRUIT_INA219_HPP__

#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <cstdint>


#define INA219_DEFAULT_ADDRESS 0x40

#define REG_CONFIG 0x00
#define REG_SHUNTVOLTAGE 0x01
#define REG_BUSVOLTAGE 0x02
#define REG_POWER 0x03
#define REG_CURRENT 0x04
#define REG_CALIBRATION 0x05

#define BUS_VOLTAGE_RANGE_32V 0x01
#define GAIN_DIV_8_320MV 0x03
#define ADC_RES_12BIT_1S 0x03
#define MODE_SANDBVOLT_CONTINUOUS 0x07

class INA219
{
public:
    INA219(int i2c_bus, int addr = INA219_DEFAULT_ADDRESS);
    ~INA219();

    void setCalibration32V2A();
    float getBusVoltage();
    float getShuntVoltage();
    float getCurrent();
    float getPower();

private:
    int fd;
    int i2c_bus;
    int addr;
    float currentLSB = 0.1; // 100uA per bit
    float powerLSB = 0.002; // 2mW per bit

    void writeRegister(int reg, int value);
    int readRegister(int reg);
};

#endif
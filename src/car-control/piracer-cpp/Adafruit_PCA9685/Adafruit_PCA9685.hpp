#pragma once
#ifndef __ADAFRUIT_PCA9685_HPP__
#define __ADAFRUIT_PCA9685_HPP__

#include <iostream>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <cmath>
#include <cstdint>
#include <string>
#include <cerrno>
#include <cstring>


// PCA9685 Register Addresses
#define PCA9685_ADDRESS     0x40
#define MODE1               0x00
#define MODE2               0x01
#define PRESCALE            0xFE
#define LED0_ON_L           0x06
#define LED0_ON_H           0x07
#define LED0_OFF_L          0x08
#define LED0_OFF_H          0x09
#define ALL_LED_ON_L        0xFA
#define ALL_LED_ON_H        0xFB
#define ALL_LED_OFF_L       0xFC
#define ALL_LED_OFF_H       0xFD

// Bit definitions
#define RESTART             0x80
#define SLEEP               0x10
#define ALLCALL             0x01
#define INVRT               0x10
#define OUTDRV              0x04

class PCA9685 
{
public:
    explicit PCA9685(int i2c_bus = 1, int address = PCA9685_ADDRESS);
    ~PCA9685();

    void setPWMFreq(float freqHz);
    void setPWM(int channel, int on, int off);
    void setAllPWM(int on, int off);

private:
    int fd;
    int i2c_bus;
    int addr;

    void writeByte(uint8_t reg, uint8_t data);
    uint8_t readByte(uint8_t reg);
};

#endif
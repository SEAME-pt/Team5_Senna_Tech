#include "Adafruit_INA219.hpp"

INA219::INA219(int i2c_bus, int addr) : i2c_bus(i2c_bus), addr(addr)
{
    std::string dev = "/dev/i2c-" + std::to_string(i2c_bus);
    fd = open(dev.c_str(), O_RDWR);
    if (fd < 0)
    {
        perror("Failed to open I2C bus");
        exit(1);
    }

    if (ioctl(fd, I2C_SLAVE, addr) < 0)
    {
        perror("Failed to set I2C address");
        exit(1);
    }

    setCalibration32V2A();
}

INA219::~INA219()
{
    if (fd >= 0)
        close(fd);
}

void INA219::setCalibration32V2A()
{
    int calValue = 4096;
    writeRegister(REG_CALIBRATION, calValue);

    int config = (BUS_VOLTAGE_RANGE_32V << 13) |
                 (GAIN_DIV_8_320MV << 11) |
                 (ADC_RES_12BIT_1S << 7) |
                 (ADC_RES_12BIT_1S << 3) |
                 MODE_SANDBVOLT_CONTINUOUS;
    writeRegister(REG_CONFIG, config);
}

float INA219::getBusVoltage()
{
    int rawBusVoltage = readRegister(REG_BUSVOLTAGE);
    return (rawBusVoltage >> 3) * 0.004;
}

float INA219::getShuntVoltage()
{
    int rawShuntVoltage = readRegister(REG_SHUNTVOLTAGE);
    return rawShuntVoltage * 0.00001;
}

float INA219::getCurrent()
{
    int rawCurrent = readRegister(REG_CURRENT);
    return rawCurrent * currentLSB;
}

float INA219::getPower()
{
    int rawPower = readRegister(REG_POWER);
    return rawPower * powerLSB;
}

void INA219::writeRegister(int reg, int value)
{
    uint8_t buf[3];
    buf[0] = reg;
    buf[1] = (value >> 8) & 0xFF;
    buf[2] = value & 0xFF;
    if (write(fd, buf, 3) != 3)
        perror("Failed to write to I2C register");
}

int INA219::readRegister(int reg)
{
    uint8_t buf[2];
    if (write(fd, &reg, 1) != 1)
    {
        perror("Failed to write register address");
        return -1;
    }
    if (read(fd, buf, 2) != 2)
    {
        perror("Failed to read from I2C register");
        return -1;
    }
    return (buf[0] << 8) | buf[1];
}
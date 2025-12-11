#include "Adafruit_PCA9685.hpp"

PCA9685::PCA9685(int i2c_bus, int addr) :
    i2c_bus(i2c_bus), addr(addr)
{
    std::string device = "/dev/i2c-" + std::to_string(i2c_bus);
    fd = open(device.c_str(), O_RDWR);
    if (fd < 0) {
        std::cerr << "Failed to open I2C bus: " << strerror(errno) << std::endl;
        exit(1);
    }

    if (ioctl(fd, I2C_SLAVE, addr) < 0) {
        std::cerr << "Failed to set I2C address: " << strerror(errno) << std::endl;
        close(fd);
        exit(1);
    }

    setAllPWM(0, 0);
    writeByte(MODE2, OUTDRV);
    writeByte(MODE1, ALLCALL);
    usleep(5000); // wait for oscillator

    int mode1 = readByte(MODE1);
    mode1 = mode1 & ~SLEEP; // Wake up (reset sleep)
    writeByte(MODE1, mode1);
    usleep(5000); // wait for oscillator
}

PCA9685::~PCA9685()
{
    if (fd >= 0) {
        close(fd);
    }
}

void PCA9685::setPWMFreq(float freqHz)
{
    float prescaleval = 25000000.0;
    prescaleval /= 4096.0;
    prescaleval /= freqHz;
    prescaleval -= 1.0;
    int prescale = std::floor(prescaleval + 0.5);

    int oldmode = readByte(MODE1);
    int newmode = (oldmode & 0x7F) | 0x10; // sleep
    writeByte(MODE1, newmode);             // go to sleep
    writeByte(PRESCALE, prescale);
    writeByte(MODE1, oldmode);
    usleep(5000);
    writeByte(MODE1, oldmode | RESTART);
}

void PCA9685::setPWM(int channel, int on, int off)
{
    writeByte(LED0_ON_L + 4 * channel, on & 0xFF);
    writeByte(LED0_ON_H + 4 * channel, on >> 8);
    writeByte(LED0_OFF_L + 4 * channel, off & 0xFF);
    writeByte(LED0_OFF_H + 4 * channel, off >> 8);
}

void PCA9685::setAllPWM(int on, int off)
{
    int x = 1;
    if (x == 1)
        std::cout << "oi";
    writeByte(ALL_LED_ON_L, on & 0xFF);
    writeByte(ALL_LED_ON_H, on >> 8);
    writeByte(ALL_LED_OFF_L, off & 0xFF);
    writeByte(ALL_LED_OFF_H, off >> 8);
}

void PCA9685::writeByte(uint8_t reg, uint8_t data)
{
    uint8_t buffer[2] = { reg, data };
    if (write(fd, buffer, 2) != 2) {
        std::cerr << "Failed to write to I2C device: " << strerror(errno) << std::endl;
    }
}

uint8_t PCA9685::readByte(uint8_t reg)
{
    if (write(fd, &reg, 1) != 1) {
        std::cerr << "Failed to set register for reading: " << strerror(errno) << std::endl;
        return 0;
    }

    uint8_t data;
    if (read(fd, &data, 1) != 1) {
        std::cerr << "Failed to read from I2C device: " << strerror(errno) << std::endl;
        return 0;
    }

    return data;
}

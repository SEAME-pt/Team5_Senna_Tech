# ThreadX Development with STM32 and ST-Link in VS Code

This guide explains how to set up, build, and flash ThreadX-based firmware to an STM32 microcontroller using ST-Link tools, all from within Visual Studio Code.

## Prerequisites
- ARM GCC toolchain (`arm-none-eabi-gcc`)
- CMake
- ST-Link tools (`stlink-tools`)

## Dependency Intalation for Debian based OS

```shell
cd scripts
chmod +x install_dependencies.sh
./scripts/install_dependencies.sh
```

## Building and Flashing Firmware

Use the compile_flash.sh script to build and flash your ThreadX project:

### Full Rebuild (Recommended for first build)

```shell
chmod +x ./compile_flash.sh
./compile_flash.sh slow
```

- Cleans and recreates the build directory
- Configures CMake with the ARM GCC toolchain
- Compiles the project
- Converts the ELF file to binary
- Flashes the binary to the STM32 using ST-Link

### Quick Rebuild (After initial setup)

```shell
./compile_flash.sh
```

If any doubt try:
```shell
./compile_flash -h
```

## Manual Build and Flash Steps

### 1. Create and enter the build directory:
```shell
mkdir build && cd build
```

### 2. Configure CMake:
```shell
cmake -DCMAKE_TOOLCHAIN_FILE=../cmake/gcc-arm-none-eabi.cmake ..
```

### 3. Compile the Project
```shell
make -j$(nproc)
```

## Flashing to STM32

### 4. Convert ELF to Binary
```shell
arm-none-eabi-objcopy -O binary SennaTech.elf SennaTech.bin
```

### 5. Verify ST-Link Connection
```shell
st-info --probe
```

Expected output should show your STM32 device information.

### 6. Erase Flash (Optional but Recommended)
```shell
st-flash erase
```

### 7. Write Binary to Flash Memory
```shell
st-flash --reset write ThreadX_Os.bin 0x08000000
```

**Parameters:**
- `0x08000000` - Flash memory start address for STM32
- `--reset` - Automatically reset the microcontroller after flashing

---

# UART Debug Messages

 - Debug messages are sent via USART1 at 115200 baud, 8N1.
 - Use a serial terminal (minicom, screen, etc.) to view output.

## 1. Connect the Board
- Use a USB cable if your board has a Virtual COM Port (e.g., ST-Link VCP)
- Or use a USB-to-Serial adapter connected to the board's UART TX/RX pins

## 2. Find the Serial Port
On Linux, run:
```sh
sudo dmesg | grep tty
```
Look for `/dev/ttyACM0`, `/dev/ttyUSB0`, or similar.

## 3. Open a Serial Terminal
You can use `minicom` or `screen`.

**minicom example:**
```sh
minicom -b 115200 -D /dev/ttyACM0
```

**screen example:**
```sh
screen /dev/ttyACM0 115200
```

## 4. UART Settings
- Baud rate: 115200
- Data bits: 8
- Parity: None
- Stop bits: 1

## 5. View Output
You should now see the debug messages printed by your firmware.

## 6. Kill UART Window
 - Press Ctrl+A then release both and press K
 - When prompted, press y to confirm exit.

---

## Summary

- Use install_dependencies.sh for setup.
- Use compile_flash.sh for building and flashing.
- All steps can be performed inside VS Code’s integrated terminal.

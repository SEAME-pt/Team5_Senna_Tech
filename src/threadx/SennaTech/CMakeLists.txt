cmake_minimum_required(VERSION 3.22)

#
# This file is generated only once,
# and is not re-generated if converter is called multiple times.
#
# User is free to modify the file as much as necessary
#

# Setup compiler settings
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)


# Define the build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Debug")
endif()

# Set the project name
set(CMAKE_PROJECT_NAME SennaTech)

# Enable compile command to ease indexing with e.g. clangd
set(CMAKE_EXPORT_COMPILE_COMMANDS TRUE)

# Core project settings
project(${CMAKE_PROJECT_NAME})
message("Build type: " ${CMAKE_BUILD_TYPE})

# Enable CMake support for ASM and C languages
enable_language(C ASM)

# Create an executable object type
add_executable(${CMAKE_PROJECT_NAME})

# Add STM32CubeMX generated sources
add_subdirectory(cmake/stm32cubemx)

# Link directories setup
target_link_directories(${CMAKE_PROJECT_NAME} PRIVATE
    # Add user defined library search paths
)

# Add sources to executable
target_sources(${CMAKE_PROJECT_NAME} PRIVATE
    # Add user sources here
    Core/Src/can/can_manager.c
    Core/Src/can/mcp2515.c
    Core/Src/car/parking_modes/final_park_instance.c
    Core/Src/car/parking_modes/first_park_instance.c
    Core/Src/car/parking_modes/parking.c
    Core/Src/car/parking_modes/second_park_instance.c
    Core/Src/car/car.c
    Core/Src/car/motor.c
    Core/Src/display/oled_designs/cute_eyes.c
    Core/Src/display/oled_designs/cute_smiling_eyes.c
    Core/Src/display/oled_designs/sleeping_eyes.c
    Core/Src/display/ssd1305.c
    Core/Src/display/oled.c
    Core/Src/i2c/battery.c
    Core/Src/i2c/i2c_hal.c
    Core/Src/i2c/ina219.c
    Core/Src/i2c/pca9685.c
    Core/Src/i2c/srf08.c
    Core/Src/pid/pid.c
    Core/Src/pid/pid_utils.c
    Core/Src/sensor/ultrasonic/thread_ultrasonic.c
    Core/Src/sensor/ultrasonic/front_ultrasonic.c
    Core/Src/sensor/ultrasonic/back_ultrasonic.c
    Core/Src/sensor/ambient_light.c
    Core/Src/sensor/microphone.c
    Core/Src/sensor/odometer.c
    Core/Src/sensor/speedsensor.c
    Core/Src/utils/debug_utils.c
    Core/Src/utils/sleep_hal.c
    Core/Src/heartbeat.c
)

# Add include paths
target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE
    # Add user defined include paths
    Core/Inc
    Core/Inc/can
    Core/Inc/car
    Core/Inc/display
    Core/Inc/i2c
    Core/Inc/pid
    Core/Inc/sensors
    Core/Inc/utils
)

# Add project symbols (macros)
target_compile_definitions(${CMAKE_PROJECT_NAME} PRIVATE
    # Add user defined symbols
)

# Remove wrong libob.a library dependency when using cpp files
list(REMOVE_ITEM CMAKE_C_IMPLICIT_LINK_LIBRARIES ob)

# Add linked libraries
target_link_libraries(${CMAKE_PROJECT_NAME}
    stm32cubemx

    # Add user defined libraries
)

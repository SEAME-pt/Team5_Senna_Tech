cmake_minimum_required(VERSION 3.15)
project(PiRacer-cpp VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- Include directories for the PiRacer sources ---
include_directories(
    ../../src/car-control/piracer-cpp/Adafruit_INA219
    ../../src/car-control/piracer-cpp/Adafruit_PCA9685
    ../../src/car-control/piracer-cpp/Gamepad
    ../../src/car-control/piracer-cpp/PiRacer
)

# --- Source files from PiRacer library ---
set(PIRACER_SRC
    ../../src/car-control/piracer-cpp/Adafruit_INA219/Adafruit_INA219.cpp
    ../../src/car-control/piracer-cpp/Adafruit_PCA9685/Adafruit_PCA9685.cpp
    ../../src/car-control/piracer-cpp/PiRacer/PiRacer.cpp
)

# ====================================================
#             GOOGLE TEST CONFIGURATION
# ====================================================

include(FetchContent)

FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/refs/heads/main.zip
)

# Makes the content available and builds GTest
FetchContent_MakeAvailable(googletest)

enable_testing()

# ====================================================
#               UNIT TEST EXECUTABLE
# ====================================================

add_executable(unittests
    motorController.cpp
    ${PIRACER_SRC}
)

# --- Link GoogleTest ---
target_link_libraries(unittests
    gtest
    gtest_main
    pthread
)


#set(GAMEPAD_SRC
#	../src/car-control/piracer.cpp/Gamepad/Joystick.cpp
#	../src/car-control/piracer.cpp/Gamepad/ShanwanGamepad.cpp
#)
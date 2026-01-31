cmake_minimum_required(VERSION 3.16)
project(Tests VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# -----------------------------------
# GoogleTest via FetchContent
# -----------------------------------
include(FetchContent)

FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
)

# Fetch and make gtest/gmock available
FetchContent_MakeAvailable(googletest)

# -----------------------------------
# Project include directories
# -----------------------------------
# INCLUIA O DIRETÓRIO PARA OS .hpp
include_directories(
    ../../src/car-control/raspberry-control/Adafruit_INA219
    ../../src/car-control/raspberry-control/Adafruit_PCA9685
    ../../src/car-control/raspberry-control/Gamepad
    ../../src/car-control/raspberry-control/PiRacer
)


# -----------------------------------
# Source files for the car-control feature
# -----------------------------------
# INCLUA OS ARQUIVOS .cpp QUE PRECISAM SER COMPILADOS
set(PIRACER_SRC
    ../../src/car-control/raspberry-control/Adafruit_INA219/Adafruit_INA219.cpp
    ../../src/car-control/raspberry-control/Adafruit_PCA9685/Adafruit_PCA9685.cpp
    ../../src/car-control/raspberry-control/PiRacer/PiRacer.cpp
)

set(GAMEPAD_SRC
    ../../src/car-control/raspberry-control/Gamepad/Joystick.cpp
    ../../src/car-control/raspberry-control/Gamepad/ShanwanGamepad.cpp
)

# -----------------------------------
# Test executable
# -----------------------------------
#INCLUDE O CAMINHO PARA OS EXECUTAVEIS DE TESTE COM OS SOURCES NECESSERAIO
add_executable(test_car_control
    test_car_control.cpp
    ${PIRACER_SRC}
)

# -----------------------------------
# Link with GoogleTest
# -----------------------------------
target_link_libraries(test_car_control
    PRIVATE
        gtest
        gtest_main
)

# -----------------------------------
# Enable CTest integration
# -----------------------------------
enable_testing()
add_test(NAME car-control-tests COMMAND test_car_control)
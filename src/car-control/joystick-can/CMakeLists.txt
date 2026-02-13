cmake_minimum_required(VERSION 3.15)
project(PiRacer-cpp VERSION 1.0 LANGUAGES CXX)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/modules/")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(
	./Gamepad
)

set(GAMEPAD_SRC
	Gamepad/Joystick.cpp
	Gamepad/ShanwanGamepad.cpp
)

add_executable(gamepad_control
	gamepad_control.cpp
	${GAMEPAD_SRC}
)

add_executable(test_move
	test_move.cpp
)

add_executable(test_autonomy
	test_autonomy.cpp
)


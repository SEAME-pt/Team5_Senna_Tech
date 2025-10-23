#pragma once
#ifndef __SHANWANGAMEPAD__HPP__
# define __SHANWANGAMEPAD__HPP__

#include "Joystick.hpp"

class Vector3f {
public:
	float x, y, z;

	Vector3f() : x(0.0f), y(0.0f), z(0.0f) {}
};

class ShanWanGamepadInput {
public:
	Vector3f analog_stick_left;
	Vector3f analog_stick_right;
	bool button_up, button_down, button_left, button_right;
	bool button_x, button_a, button_b, button_y;
	bool button_l1, button_l2, button_l3, button_r1, button_r2, button_r3;
	bool button_select, button_start, button_home;

	ShanWanGamepadInput()
		: button_up(false), button_down(false), button_left(false), button_right(false),
		  button_l1(false), button_l2(false), button_l3(false),
		  button_r1(false), button_r2(false), button_r3(false),
		  button_x(false), button_a(false), button_b(false), button_y(false),
		  button_select(false), button_start(false), button_home(false) {}
};

class ShanWanGamepad : public Joystick {
public:
	ShanWanGamepadInput gamepad_input;

	ShanWanGamepad();
	ShanWanGamepad(const std::string& dev_fn);
	ShanWanGamepad(const std::string& dev_fn, bool non_block);
	ShanWanGamepadInput read_data();
};

#endif
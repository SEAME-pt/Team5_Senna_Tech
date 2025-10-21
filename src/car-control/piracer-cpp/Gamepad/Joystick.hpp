#pragma once
#ifndef __JOYSTICK_HPP__
# define __JOYSTICK_HPP__

#include <fcntl.h>
#include <linux/joystick.h>
#include <unistd.h>
#include <iostream>
#include <cstring>
#include <vector>
#include <unordered_map>
#include <tuple>
#include <sys/epoll.h>

#define BLOCK 0
#define NONBLOCK 1

class Joystick 
{
public:
	std::unordered_map<std::string, float> axis_states;
	std::unordered_map<std::string, int> button_states;
	std::unordered_map<int, std::string> axis_names;
	std::unordered_map<int, std::string> button_names;
	std::vector<std::string> axis_map;
	std::vector<std::string> button_map;
	int num_axes;
	int num_buttons;
	std::string dev_fn;
	std::string js_name;
	int jsdev;
	int epoll_fd;
	bool non_block;

	Joystick(const std::string& dev_fn, bool nonblock);
	~Joystick();

	bool init();
	void show_map();
	std::tuple<std::string, int, int, std::string, int, float>poll();
};

#endif
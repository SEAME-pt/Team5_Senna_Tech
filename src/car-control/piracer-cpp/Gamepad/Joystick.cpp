#include "Joystick.hpp"

Joystick::Joystick(const std::string& dev_fn = "/dev/input/js0", bool non_block = false):
	dev_fn(dev_fn),
	jsdev(-1),
	epoll_fd(-1),
	num_axes(0),
	num_buttons(0),
	non_block(non_block)
{
	// Initialize the axis and button names maps with standard values
	axis_names[0x00] = "x";
	axis_names[0x01] = "y";
	axis_names[0x02] = "z";
	axis_names[0x03] = "rx";
	axis_names[0x04] = "ry";
	axis_names[0x05] = "rz";
	axis_names[0x10] = "hat0x";
	axis_names[0x11] = "hat0y";

	button_names[0x120] = "A";
	button_names[0x121] = "B";
	button_names[0x122] = "X";
	button_names[0x123] = "Y";
	button_names[0x124] = "TL";
	button_names[0x125] = "TR";
	button_names[0x126] = "TL2";
	button_names[0x127] = "TR2";
	button_names[0x128] = "Select";
	button_names[0x129] = "Start";
	button_names[0x12A] = "Mode";
	button_names[0x12B] = "ThumbL";
	button_names[0x12C] = "ThumbR";
}

bool Joystick::init() 
{
	if (access(dev_fn.c_str(), F_OK) == -1)
		return false;

	jsdev = open(dev_fn.c_str(), O_RDONLY);
	if (jsdev == -1)
		return false;

	char name[128];
	if (ioctl(jsdev, JSIOCGNAME(sizeof(name)), name) < 0)
		strncpy(name, "Unknown", sizeof(name));
	js_name = name;

	ioctl(jsdev, JSIOCGAXES, &num_axes);
	ioctl(jsdev, JSIOCGBUTTONS, &num_buttons);

	__u8 axis_map[ABS_MAX + 1];
	ioctl(jsdev, JSIOCGAXMAP, axis_map);
	for (int i = 0; i < num_axes; ++i)
	{
		std::string axis_name = axis_names[axis_map[i]];
		this->axis_map.push_back(axis_name);
		axis_states[axis_name] = 0.0f;
	}

	__u16 button_map[KEY_MAX - BTN_MISC + 1];
	ioctl(jsdev, JSIOCGBTNMAP, button_map);
	for (int i = 0; i < num_buttons; ++i)
	{
		std::string button_name = button_names[button_map[i]];
		this->button_map.push_back(button_name);
		button_states[button_name] = 0;
	}

	if (non_block)
	{
		epoll_fd = epoll_create1(0);
		if (epoll_fd == -1)
		{
			close(jsdev);
			return false;
		}

		epoll_event ev;
		ev.events = EPOLLIN;
		ev.data.fd = jsdev;
		if (epoll_ctl(epoll_fd, EPOLL_CTL_ADD, jsdev, &ev) == -1)
		{
			close(jsdev);
			close(epoll_fd);
			return false;
		}
	}

	return true;
}

void Joystick::show_map() 
{
	std::cout << num_axes << " axes found: ";
	for (const auto& axis : axis_map)
		std::cout << axis << " ";
	std::cout << std::endl;

	std::cout << num_buttons << " buttons found: ";
	for (const auto& button : button_map)
		std::cout << button << " ";
	std::cout << std::endl;
}

std::tuple<std::string, int, int, std::string, int, float> Joystick::poll() 
{
	std::string button_name;
	int button_number = -1;
	int button_state = -1;
	std::string axis_name;
	int axis_number = -1;
	float axis_val = 0.0f;

	if (jsdev == -1)
		return std::make_tuple(button_name, button_number, button_state, axis_name, axis_number, axis_val);

	if (non_block)
	{
		epoll_event events[1];
		int nfds = epoll_wait(epoll_fd, events, 1, 10); // 10 milliseconds timeout

		if (nfds == -1)
		{
			perror("epoll_wait");
			return std::make_tuple(button_name, button_number, button_state, axis_name, axis_number, axis_val);
		}

		if (nfds == 0)
			// No data within 10 milliseconds
			return std::make_tuple(button_name, button_number, button_state, axis_name, axis_number, axis_val);
	}

	js_event ev;
	ssize_t bytes = read(jsdev, &ev, sizeof(ev));

	if (bytes == sizeof(ev)) {
		if (ev.type & JS_EVENT_INIT)
			return std::make_tuple(button_name, button_number, button_state, axis_name, axis_number, axis_val);

		if (ev.type == JS_EVENT_BUTTON)
		{
			button_name = button_names[ev.number];
			button_states[button_name] = ev.value;
			button_number = ev.number;
			button_state = ev.value;
		}

		if (ev.type == JS_EVENT_AXIS)
		{
			axis_name = axis_names[ev.number];
			axis_states[axis_name] = ev.value / 32767.0f;
			axis_number = ev.number;
			axis_val = ev.value / 32767.0f;
		}
	}

	return std::make_tuple(button_name, button_number, button_state, axis_name, axis_number, axis_val);
}

Joystick::~Joystick()
{
	if (jsdev != -1) close(jsdev);
	if (epoll_fd != -1) close(epoll_fd);
}
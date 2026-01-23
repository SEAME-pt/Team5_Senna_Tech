#include "Gamepad/ShanwanGamepad.hpp"
#include "canSocket.cpp"
#define CAN_ID_STEERING  0x110
#define CAN_ID_THROTTLE  0x100

int open_can_socket(const char *ifname)
{
	int sock = socket(PF_CAN, SOCK_RAW, CAN_RAW);
	if (sock < 0)
	{
		perror("socket");
		return -1;
	}

	struct ifreq ifr;
	std::strncpy(ifr.ifr_name, ifname, IFNAMSIZ);
	if (ioctl(sock, SIOCGIFINDEX, &ifr) < 0)
	{
		perror("ioctl");
		return -1;
	}

	struct sockaddr_can addr;
	std::memset(&addr, 0, sizeof(addr));
	addr.can_family  = AF_CAN;
	addr.can_ifindex = ifr.ifr_ifindex;

	if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0)
	{
		perror("bind");
		return -1;
	}

	return sock;
}

void send_int16(int socket, uint32_t can_id, int16_t value)
{
	struct can_frame frame;

	frame.can_id  = can_id;
	frame.can_dlc = 2;

	frame.data[0] = (value >> 8) & 0xFF;
	frame.data[1] = value & 0xFF;

	if (write(socket, &frame, sizeof(frame)) != sizeof(frame))
		perror("CAN write");
}

int main()
{
    try {
        ShanWanGamepad gamepad;

        CanSocket can("can0");  
        int sock = can.getSock();

        while (true)
        {
            ShanWanGamepadInput input = gamepad.read_data();

            float steering = input.analog_stick_right.x;
            float throttle = input.analog_stick_left.y;

            int16_t steering_can = static_cast<int16_t>(steering * 32767);
            int16_t throttle_can = static_cast<int16_t>(throttle * 32767);

            send_int16(sock, CAN_ID_STEERING, steering_can);
            send_int16(sock, CAN_ID_THROTTLE, throttle_can);

            std::cout << "Steering: " << steering
                      << " | Throttle: " << throttle
                      << std::endl;
        }

    } catch (const std::exception& e) {
        std::cerr << "Error initializing CAN or Gamepad: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
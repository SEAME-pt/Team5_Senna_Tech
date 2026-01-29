#include <iostream>
#include <string>
#include <cstring>
#include <stdexcept>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <net/if.h>
#include <linux/can.h>
#include <linux/can/raw.h>

class CanSocket {
public:
    explicit CanSocket(const std::string& interface_name) {
        sock = ::socket(PF_CAN, SOCK_RAW, CAN_RAW);
        if (sock < 0) {
            throw std::runtime_error("Failed to create CAN socket");
        }

        ifreq ifr{};
        std::strncpy(ifr.ifr_name, interface_name.c_str(), IFNAMSIZ - 1);
        ifr.ifr_name[IFNAMSIZ - 1] = '\0';

        if (ioctl(sock, SIOCGIFINDEX, &ifr) < 0) {
            ::close(sock);
            throw std::runtime_error("Failed to get interface index for " + interface_name);
        }

        sockaddr_can addr{};
        addr.can_family  = AF_CAN;
        addr.can_ifindex = ifr.ifr_ifindex;

        if (bind(sock, reinterpret_cast<sockaddr*>(&addr), sizeof(addr)) < 0) {
            ::close(sock);
            throw std::runtime_error("Failed to bind CAN socket to " + interface_name);
        }
    }

    ~CanSocket() {
        if (sock >= 0) ::close(sock);
    }

    int getSock() const { return sock; }

private:
    int sock{-1};
};
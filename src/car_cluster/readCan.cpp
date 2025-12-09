#include <iostream>
#include <unistd.h>
#include <sys/socket.h>
#include <linux/can.h>
#include <linux/can/raw.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <cstring>

int main() {
    int sock = socket(PF_CAN, SOCK_RAW, CAN_RAW);
    if (sock < 0) {
        perror("Error opening CANsocket");
        return 1;
    }

    struct ifreq ifr;
    std::strcpy(ifr.ifr_name, "can0");
    ioctl(sock, SIOCGIFINDEX, &ifr);

    struct sockaddr_can addr{};
    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;

    if (bind(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("Error binding socket CAN");
        return 1;
    }

    std::cout << "Waiting messages CAN...\n";

    struct can_frame frame;
    while (true) {
        int nbytes = read(sock, &frame, sizeof(frame));
        if (nbytes > 0) {
            std::cout << "ID: 0x" << std::hex << frame.can_id
                      << " DLC: " << std::dec << (int)frame.can_dlc
                      << " DATA: ";
            for (int i = 0; i < frame.can_dlc; i++)
                std::cout << (int)frame.data[i] << " ";
            std::cout << "\n";
        }
    }

    close(sock);
    return 0;
}

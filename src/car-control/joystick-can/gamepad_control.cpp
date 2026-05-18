#include "Gamepad/ShanwanGamepad.hpp"
#include "canSocket.cpp"
#include <thread>
#include <chrono>
#include <cmath>

#define CAN_ID_JOY_MOVEMENT   0x001
#define CAN_ID_MODE_MOVEMENT  0x003

void send_drive(int socket, uint32_t can_id, int16_t throttle, int16_t steering)
{
    struct can_frame frame{};
    frame.can_id  = can_id;
    frame.can_dlc = 4;

    frame.data[0] = throttle & 0xFF;
    frame.data[1] = (throttle >> 8) & 0xFF;

    frame.data[2] = steering & 0xFF;
    frame.data[3] = (steering >> 8) & 0xFF;

    if (write(socket, &frame, sizeof(frame)) != sizeof(frame))
        perror("CAN write drive");
}

void send_int16(int socket, uint32_t can_id, int16_t value)
{
    struct can_frame frame{};
    frame.can_id  = can_id;
    frame.can_dlc = 2;

    frame.data[0] = value & 0xFF;
    frame.data[1] = (value >> 8) & 0xFF;

    if (write(socket, &frame, sizeof(frame)) != sizeof(frame))
        perror("CAN write");
}

static int16_t raw_from_percent_int16(float percent)
{
    if (percent > 1.0f)  percent = 1.0f;
    if (percent < -1.0f) percent = -1.0f;
    return static_cast<int16_t>(percent * 100.0f);
}

int main()
{
    try {
        ShanWanGamepad gamepad;
        CanSocket can("can0");

        int sock = can.getSock();

        bool auto_mode = false;
        bool debug = false;
        static int16_t last_throttle = 0;
        static int16_t last_steering = 0;

        while (true)
        {
            ShanWanGamepadInput input = gamepad.read_data();

            float steering = input.analog_stick_right.x;
            float throttle = input.analog_stick_left.y;

            int16_t steering_can = raw_from_percent_int16(steering);
            int16_t throttle_can = raw_from_percent_int16(throttle);

            bool joystick_active =
                (std::abs(steering) > 0.05f || std::abs(throttle) > 0.05f);

            // ===== MODE CONTROL =====
            if (input.button_a) {
                send_int16(sock, CAN_ID_MODE_MOVEMENT, 0); // AUTO
                auto_mode = true;
                debug = false;
                printf("Mode: AUTO\n");
            }
            else if (input.button_b) {
                send_int16(sock, CAN_ID_MODE_MOVEMENT, 2); // DEBUG
                debug = true;
                auto_mode = false;
                printf("Mode: DEBUG\n");
            }

            // joystick overrides AUTO → MANUAL
            if (joystick_active && auto_mode) {
                send_int16(sock, CAN_ID_MODE_MOVEMENT, 1); // MANUAL
                auto_mode = false;
                debug = false;
                printf("Auto -> Manual (joystick)\n");
            }

            // ===== DRIVE =====
            if (!auto_mode) {

                bool changed =
                    (throttle_can != last_throttle ||
                     steering_can != last_steering);

                if (changed) {
                    send_drive(sock, CAN_ID_JOY_MOVEMENT, throttle_can, steering_can);

                    last_throttle = throttle_can;
                    last_steering = steering_can;
                }
            }

            const char* current_mode =
                auto_mode ? "AUTO" : (debug ? "DEBUG" : "MANUAL");

            printf(
                "Mode: %-6s | S: %6.2f -> %4d | T: %6.2f -> %4d\n",
                current_mode,
                steering, steering_can,
                throttle, throttle_can
            );

            std::this_thread::sleep_for(std::chrono::milliseconds(15));
        }

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
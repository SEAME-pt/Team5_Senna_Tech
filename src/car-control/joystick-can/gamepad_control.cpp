#include "Gamepad/ShanwanGamepad.hpp"
#include "canSocket.cpp"
#include <thread>
#include <chrono>
#define CAN_ID_STEERING  0x110
#define CAN_ID_THROTTLE  0x100
#define CAN_ID_MODE      0x105

void send_int16(int socket, uint32_t can_id, int16_t value)
{
    struct can_frame frame{};
    frame.can_id  = can_id;
    frame.can_dlc = 2;

    uint16_t raw = static_cast<uint16_t>(value);

    // Intel / little-endian
    frame.data[0] = raw & 0xFF;        // LSB
    frame.data[1] = (raw >> 8) & 0xFF; // MSB

    printf("[TX] ID: 0x%X | Raw: %d | Bytes: %02X %02X\n",
           can_id, value, frame.data[0], frame.data[1]);

    if (write(socket, &frame, sizeof(frame)) != sizeof(frame))
        perror("CAN write");
}

// Mapeia de -1.0..1.0 para -100..100
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
        int debug = false;
        int auto_mode = false;

        while (true)
        {
            ShanWanGamepadInput input = gamepad.read_data();
            
            if (input.button_a) {
                send_int16(sock, CAN_ID_MODE, 0); // Autonomous Mode (A)
                auto_mode = true;
                printf("Mode: AUTO\n");
            }
            else if (input.button_l1) {
                send_int16(sock, CAN_ID_MODE, 1); // Manual Mode (Y)
                debug = false;
                auto_mode = false;
                printf("Mode: MANUAL\n");
            }
            else if (input.button_b) {
                send_int16(sock, CAN_ID_MODE, 2); // Debug Mode (B)
                debug = true;
                auto_mode = false;
                printf("Mode: DEBUG\n");
            }

            float steering  = input.analog_stick_right.x; // -1.0 .. 1.0
            float throttle  = input.analog_stick_left.y;  // -1.0 .. 1.0

            // Mapear para int16
            int16_t steering_can = raw_from_percent_int16(steering);
            int16_t throttle_can = raw_from_percent_int16(throttle);
            
            if (!auto_mode || !debug) {
                send_int16(sock, CAN_ID_STEERING, steering_can);
                send_int16(sock, CAN_ID_THROTTLE, throttle_can);
            }

            const char* current_mode = auto_mode ? "AUTO" : (debug ? "DEBUG" : "MANUAL");
            printf(
                "Mode: %-6s | Steering: %6.2f -> %4d | Throttle: %6.2f -> %4d\n",
                current_mode,
                steering, steering_can,
                throttle, throttle_can
            );
            std::this_thread::sleep_for(std::chrono::milliseconds(20));
        }
        

    } catch (const std::exception& e) {
        std::cerr << "Error initializing CAN or Gamepad: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}

/* #include <chrono>

using namespace std::chrono;

int main()
{
    try {
        ShanWanGamepad gamepad;
        CanSocket can("can0");  
        int sock = can.getSock();

        auto last_input_time = steady_clock::now();
        const auto TIMEOUT = milliseconds(200); // 200 ms sem input -> fail-safe

        while (true)
        {
            ShanWanGamepadInput input;
            bool ok = gamepad.try_read_data(input); // supondo que exista um método que retorna false se desconectado

            if (ok) {
                last_input_time = steady_clock::now();

                float steering  = input.analog_stick_right.x; 
                float throttle  = input.analog_stick_left.y;  

                int16_t steering_can = raw_from_percent_int16(steering);
                int16_t throttle_can = raw_from_percent_int16(throttle);
                
                send_int16(sock, CAN_ID_STEERING, steering_can);
                send_int16(sock, CAN_ID_THROTTLE, throttle_can);

                printf(
                    "Steer: %.2f (%d) | Throttle: %.2f (%d)\n",
                    steering, steering_can,
                    throttle, throttle_can
                );
            }
            else {
                // Falha: joystick desconectado
                auto now = steady_clock::now();
                if (now - last_input_time > TIMEOUT) {
                    // Envia comandos neutros para segurança
                    send_int16(sock, CAN_ID_STEERING, 0);
                    send_int16(sock, CAN_ID_THROTTLE, 0);
                    printf("Joystick disconnected! Motors stopped.\n");
                }
            }
        }

    } catch (const std::exception& e) {
        std::cerr << "Error initializing CAN or Gamepad: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
 */

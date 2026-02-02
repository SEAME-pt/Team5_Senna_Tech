#include "Gamepad/ShanwanGamepad.hpp"
#include "canSocket.cpp"
#define CAN_ID_STEERING  0x110
#define CAN_ID_THROTTLE  0x100

void send_int16(int socket, uint32_t can_id, int16_t value)
{
    struct can_frame frame{};
    frame.can_id  = can_id;
    frame.can_dlc = 2;

    // Usamos máscaras explícitas e garantimos que o valor 
    // seja tratado como unsigned antes de entrar no array de dados
    frame.data[0] = static_cast<uint8_t>((static_cast<uint16_t>(value) >> 8) & 0xFF);
    frame.data[1] = static_cast<uint8_t>(static_cast<uint16_t>(value) & 0xFF);

    printf("[TX] ID: 0x%X | Value: %d | Bytes: %02X %02X\n",
           can_id, value, frame.data[0], frame.data[1]);

    if (write(socket, &frame, sizeof(frame)) != sizeof(frame))
        perror("CAN write");
}

// Mapeia de -1.0..1.0 para -32767..32767
static int16_t raw_from_percent_int16(float percent)
{
    if (percent > 1.0f)  percent = 1.0f;
    if (percent < -1.0f) percent = -1.0f;

    return static_cast<int16_t>(percent * 32767.0f + (percent >= 0 ? 0.5f : -0.5f));
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

            float steering  = input.analog_stick_right.x; // -1.0 .. 1.0
            float throttle  = input.analog_stick_left.y;  // -1.0 .. 1.0

            // Mapear para int16
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

    } catch (const std::exception& e) {
        std::cerr << "Error initializing CAN or Gamepad: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
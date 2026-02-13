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

/*     printf("[TX] ID: 0x%X | Value: %d | Bytes: %02X %02X\n",
           can_id, value, frame.data[0], frame.data[1]); */

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

void    move(int sock, uint32_t ID, float percent)
{
    int16_t can_raw;

    can_raw = raw_from_percent_int16(percent);
    send_int16(sock, ID, can_raw);
    
    // PRINTS
    std::cout << "ID: " << ID << std::endl;
    std::cout << "PERCENT: " << percent << std::endl;
    std::cout << "CAN RAW: " << can_raw << std::endl;
    sleep(1);
}

// MAIN PARA TESTES DE COMANDOS
int main()
{
    try {

        CanSocket can("can0");  
        int sock = can.getSock();

        while (true)
        {

            move(sock, CAN_ID_STEERING, 0.5f);

            move(sock, CAN_ID_STEERING, 1.0f);

            move(sock, CAN_ID_STEERING, -0.5f);

            move(sock, CAN_ID_STEERING, -1.0f);
            
            move(sock, CAN_ID_STEERING, 0.0f);
            break;
        }

    } catch (const std::exception& e) {
        std::cerr << "Error initializing CAN" << e.what() << std::endl;
        return 1;
    }

    return 0;
}
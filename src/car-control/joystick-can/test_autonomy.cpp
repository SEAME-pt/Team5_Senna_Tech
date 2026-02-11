#include "Gamepad/ShanwanGamepad.hpp"
#include "canSocket.cpp"
#include <chrono>
#define CAN_ID_STEERING  0x110
#define CAN_ID_THROTTLE  0x100
#define CAN_ID_BATTERY 0x200

uint8_t read_battery(int sock)
{
    struct can_frame frame{};
    uint8_t last_battery = 0;
    bool received = false;

    // Tenta ler todas as mensagens acumuladas no buffer
    // MSG_DONTWAIT impede que o loop trave se o buffer esvaziar
    while (recv(sock, &frame, sizeof(frame), MSG_DONTWAIT) > 0) 
    {
        if (frame.can_id == CAN_ID_BATTERY && frame.can_dlc == 1) 
        {
            last_battery = frame.data[0];
            received = true;
        }
    }

    if (received) {
        std::cout << "[BAT] Atualizada: " << static_cast<int>(last_battery) << "%\n";
        return last_battery;
    }

    // Se não tinha nada novo no buffer, faz uma leitura bloqueante para esperar a próxima
    ssize_t nbytes = read(sock, &frame, sizeof(frame));
    if (nbytes > 0 && frame.can_dlc == 1) {
        return frame.data[0];
    }

    return 0; 
}

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
    sleep(2);
}

// MAIN PARA TESTES DE COMANDOS
int main()
{
    try {
        CanSocket can("can0");
        int sock = can.getSock();

        struct can_filter filter;
        filter.can_id   = CAN_ID_BATTERY;
        filter.can_mask = CAN_SFF_MASK;

        setsockopt(sock, SOL_CAN_RAW, CAN_RAW_FILTER, &filter, sizeof(filter));

        move(sock, CAN_ID_THROTTLE, 0.9f);
        move(sock, CAN_ID_STEERING, 0.5f);
        move(sock, CAN_ID_STEERING, 1.0f);
        move(sock, CAN_ID_STEERING, 0.0f);
        move(sock, CAN_ID_THROTTLE, 0.0f);
        move(sock, CAN_ID_THROTTLE, -1.0f);
        sleep(2);

        uint8_t batteryStart = read_battery(sock);
        uint8_t battery = batteryStart;
        std::cout << "[BAT] INICIAL: " << static_cast<int>(batteryStart) << "%\n";
        
        // 🔹 start timer
        auto start = std::chrono::steady_clock::now();
        
        while (batteryStart <= battery + 4)
        {
            move(sock, CAN_ID_THROTTLE, 0.9f);
            move(sock, CAN_ID_STEERING, 0.5f);
            move(sock, CAN_ID_STEERING, 1.0f);
            move(sock, CAN_ID_STEERING, -0.5f);
            move(sock, CAN_ID_STEERING, -1.0f);
            move(sock, CAN_ID_STEERING, 0.0f);
            move(sock, CAN_ID_THROTTLE, 0.0f);

            battery = read_battery(sock);
        }

        auto end = std::chrono::steady_clock::now();

        auto elapsed =
            std::chrono::duration_cast<std::chrono::seconds>(end - start);

        std::cout << "Tempo de execução: "
                  << elapsed.count()
                  << " segundos\n";
    }
    catch (const std::exception& e) {
        std::cerr << "Error initializing CAN " << e.what() << std::endl;
        return 1;
    }
}


/* 
    Media de 6km/h -> 1,66 m/s

    50 segundos * 1,6m  - > 80m * 100 = 8km
*/
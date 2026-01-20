#include "can_manager.h"
#include <stdio.h> // Para printf

// Definições físicas do PiRacer
#define WHEEL_DIAMETER_M      0.065f   // 65mm
#define PULSES_PER_REV        20.0f    // Disco de 20 furos
#define PI                    3.14159f
#define TRANSMISSION_RATIO    1.0f

// Instância global do estado do veículo
volatile VehicleState_t vehicle_state = {0};


// Variáveis externas (contadores vindos do sensor, por exemplo)
extern volatile uint32_t pulse_count; 

// Função que encapsula a matemática
void update_speed_physics(uint32_t delta_time_ms) {
    static uint32_t last_pulse_count_local = 0;
    uint32_t current_pulses;

    TX_INTERRUPT_SAVE_AREA
    TX_DISABLE;
    current_pulses = pulse_count;
    TX_RESTORE;

    // cálculo do Delta
    uint32_t delta_d = current_pulses - last_pulse_count_local;
    last_pulse_count_local = current_pulses; // Atualiza referência

    // evita divisão por zero
    if (delta_time_ms == 0) return;

    float rpm = ((float)delta_p / PULSES_PER_REV) * (60000.0f / (float)delta_time_ms);
    float circumference = WHEEL_DIAMETER_M * PI;
    float speed_kmh = rpm * circumference * 0.06f;

    //Atualiza o Estado Global
    vehicle_state.speed_pulses = current_pulses; // Raw
    vehicle_state.speed_kmh = speed_kmh;         // calculated (adicione isso na struct .h)
}

static void send_speed_msg(void) {
    CAN_Frame frame;
    frame.id = CAN_ID_SPEED;
    frame.dlc = 2;

    // Converte float para int com 2 casas decimais (12.34 km/h -> 1234)
    // Isso é padrão na indústria para não enviar float via CAN
    uint16_t speed_fixed = (uint16_t)(vehicle_state.speed_kmh * 100);

    frame.data[0] = (speed_fixed >> 8) & 0xFF;
    frame.data[1] = (speed_fixed) & 0xFF;

    MCP2515_SendMessage(&frame);
}

// !!!aqui é só exemplo, vou ter que escrever as outras funcoes qu enao sao da velocidade!!
static void send_battery_msg(void) {
    CAN_Frame frame;
    frame.id = CAN_ID_BATTERY;
    frame.dlc = 1;
    // Simulação de leitura
    vehicle_state.battery_level = 85; 
    frame.data[0] = vehicle_state.battery_level;

    MCP2515_SendMessage(&frame);
}

// --- Thread de Recepção (RX) - Alta Prioridade ---
// Fica bloqueada (dormindo) até o pino INT do MCP2515 cair.
void CAN_Rx_Thread_Entry(ULONG thread_input) {
    CAN_Frame rx_frame;

    while(1) {
        // Espera a interrupção (Semáforo). 
        // Zero consumo de CPU aqui.
        tx_semaphore_get(&rx_sem, TX_WAIT_FOREVER);

        // Acordou! Pega o Mutex para usar o SPI.
        tx_mutex_get(&spi_mutex, TX_WAIT_FOREVER);

        // Esvazia o buffer do MCP2515
        while (MCP2515_ReceiveMessage(&rx_frame) == HAL_OK) {
            
            // Roteador de mensagens
            switch (rx_frame.id) {
                case CAN_ID_MOTOR_CMD:
                    vehicle_state.motor_cmd = rx_frame.data[0];
                    // Atuar no hardware aqui (ex: TIM->CCR1 = ...)
                    break;

                case CAN_ID_STEER_CMD:
                    vehicle_state.steer_angle = rx_frame.data[0];
                    // Atuar no servo aqui
                    break;
                
                // NOVO ID NO FUTURO? Adicione "case CAN_ID_NOVO:" aqui.
            }
        }

        // 4. Devolve o Mutex
        tx_mutex_put(&spi_mutex);
        
        // Acho que aqui tem que limpar a flag de interrupcao, ver nos testes
    }
}

// --- Thread de Envio (TX) - Média Prioridade ---
// Gerencia o tempo de envio de cada mensagem.
void CAN_Tx_Thread_Entry(ULONG thread_input) {
    
    ULONG last_wake_time = tx_time_get();

    tx_mutex_get(&spi_mutex, TX_WAIT_FOREVER);
    MCP2515_Reset();
    MCP2515_SetBitrate(CAN_500KBPS, MCP_8MHZ);
    MCP2515_SetNormalMode();
    tx_mutex_put(&spi_mutex);

    while(1) {
        tx_thread_sleep(10); // Assumindo Tick = 10ms
        
        ULONG now = tx_time_get();
        uint32_t time_diff_ms = (now - last_wake_time) * 10;

        // isso roda fora do Mutex do SPI, liberando o bus para RX
        update_speed_physics(time_diff_ms);

        // enviar Velocidade (prioridade alta)
        tx_mutex_get(&spi_mutex, TX_WAIT_FOREVER);
        send_speed_msg();
        tx_mutex_put(&spi_mutex);

        // enviar bateria prioridade baixa (!!!só exemplo, falta implementar o que nao é velocidade!!!)
        if (now - last_bat_tx > 100) {
            tx_mutex_get(&spi_mutex, TX_WAIT_FOREVER);
            send_battery_msg();
            tx_mutex_put(&spi_mutex);
            last_bat_tx = now;
        }

        last_wake_time = now;
    }
}

// Função chamada pela Interrupção Externa (GPIO IRQ)
void CAN_ISR_Handler(void) {
    // Avisa a Thread RX que tem trabalho
    tx_semaphore_put(&rx_sem);
}
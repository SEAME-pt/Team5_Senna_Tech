#include "can_manager.h"
#include <stdio.h> // Para printf

// Definições físicas do PiRacer
#define PULSES_PER_REV        20.0f    // Disco de 20 furos
#define PI                    3.14159f
#define TRANSMISSION_RATIO    1.0f

// Instância global do estado do veículo
volatile VehicleState_t vehicle_state = {0};


// Variáveis externas (contadores vindos do sensor, por exemplo)
extern volatile uint32_t pulse_count;

// THREADX VARIABLES
TX_MUTEX spi_mutex;       // Protege o MCP2515
TX_SEMAPHORE rx_sem;

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
    
    tx_mutex_get(&spi_mutex, TX_WAIT_FOREVER);
    MCP2515_Reset();
    MCP2515_SetBitrate(CAN_500KBPS, MCP_8MHZ);
    MCP2515_SetNormalMode();
    tx_mutex_put(&spi_mutex);

    CAN_Frame frame;

    printf("TX THREAD STARTED");
    while (1)
    {
        tx_queue_receive(&g_tx_data_queue, &frame, TX_WAIT_FOREVER);

        tx_mutex_get(&spi_mutex, TX_WAIT_FOREVER);
        MCP2515_SendMessage(&frame);
        tx_mutex_put(&spi_mutex);
    }
}

// Função chamada pela Interrupção Externa (GPIO IRQ)
void CAN_ISR_Handler(void) {
    // Avisa a Thread RX que tem trabalho
    tx_semaphore_put(&rx_sem);
}

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
void CAN_Rx_Thread_Entry(ULONG thread_input)
{
	CAN_Frame rx_frame;
	CAN_Frame local_copy;

    log_debug("CAN RX STARTED THREAD");
    while (1)
    {
        tx_semaphore_get(&rx_sem, TX_WAIT_FOREVER);
        tx_mutex_get(&spi_mutex, TX_WAIT_FOREVER);

        while (MCP2515_ReceiveMessage(&rx_frame) == HAL_OK)
        {
            memcpy(&local_copy, &rx_frame, sizeof(CAN_Frame));
            // log_debug("ID: 0x%X, DLC: %u, Data[0]: %u, Data[1]: %u", rx_frame.id, rx_frame.dlc, rx_frame.data[0], rx_frame.data[0]);
            if (tx_queue_send(&g_rx_data_queue, &local_copy, TX_NO_WAIT) != TX_SUCCESS)
            {
                log_debug("RX QUEUE FULL");
            }
        }

        tx_mutex_put(&spi_mutex);

        tx_thread_sleep(1);
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

    log_debug("TX THREAD STARTED");
    while (1)
    {
        tx_queue_receive(&g_tx_data_queue, &frame, TX_WAIT_FOREVER);

        tx_mutex_get(&spi_mutex, TX_WAIT_FOREVER);
        // log_debug("ID: 0x%X, DLC: %u, Data[0]: %u", frame.id, frame.dlc, frame.data[0]);
        MCP2515_SendMessage(&frame);
        tx_mutex_put(&spi_mutex);
        tx_thread_sleep(1);
    }
}

// Função chamada pela Interrupção Externa (GPIO IRQ)
void CAN_ISR_Handler(void) {
    // Avisa a Thread RX que tem trabalho
    tx_semaphore_put(&rx_sem);
}

void heartbeat_thread_entry(ULONG thread_input)
{
    CAN_Frame hb_frame;
    hb_frame.id = CAN_ID_HEARTBEAT;
    hb_frame.dlc = 1;
    hb_frame.data[0] = 0xAA;

    log_debug("HEARTBEAT THREAD STARTED");

    while(1)
    {
        tx_queue_send(&g_tx_data_queue, &hb_frame, TX_NO_WAIT);

        tx_thread_sleep(100);
    }
}

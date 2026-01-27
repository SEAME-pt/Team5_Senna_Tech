#ifndef CAN_MANAGER_H_
#define CAN_MANAGER_H_

#include "main.h"
#include "mcp2515.h"
#include "app_threadx.h"

// --- Definição dos IDs CAN  ---
#define CAN_ID_ESTOP        0x001
#define CAN_ID_SPEED        0x10
#define CAN_ID_MOTOR_CMD    0x100
#define CAN_ID_STEER_CMD    0x110
#define CAN_ID_BATTERY      0x200
#define CAN_ID_TEMP         0x210

// --- Estrutura global ---
typedef struct {
    // Sensores (TX - Sai do STM32)
    uint32_t speed_pulses;
    float    speed_kmh;
    uint8_t  battery_level;
    float    temperature;

    // Atuadores (RX - Entra no STM32)
    uint8_t  motor_cmd;
    uint8_t  steer_angle;
} VehicleState_t;

// Variável global acessível por todo o projeto
extern volatile VehicleState_t vehicle_state;

// --- Controle de Concorrência (Externos para o app_threadx ver) ---
extern TX_MUTEX spi_mutex;       // Protege o MCP2515
extern TX_SEMAPHORE rx_sem;      // Avisa que chegou dado (Interrupção)

// --- Funções Públicas ---
void CAN_Manager_Init(void);
void CAN_Tx_Thread_Entry(ULONG thread_input);
void CAN_Rx_Thread_Entry(ULONG thread_input);
void CAN_ISR_Handler(void); // Chama isso dentro do HAL_GPIO_EXTI_Callback

#endif

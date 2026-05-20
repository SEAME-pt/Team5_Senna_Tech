/*
 * mcp2515.h
 *
 *  Created on: Nov 18, 2025
 *      Author: Yasmine
 */

#ifndef MCP2515_H_
#define MCP2515_H_

#include "main.h"
#include "app_threadx.h"

#define MCP2515_CS_LOW()   HAL_GPIO_WritePin(GPIOE, GPIO_PIN_12, GPIO_PIN_RESET)
#define MCP2515_CS_HIGH()  HAL_GPIO_WritePin(GPIOE, GPIO_PIN_12, GPIO_PIN_SET)

// SPI commands
#define MCP_RESET     0xC0
#define MCP_READ      0x03
#define MCP_WRITE     0x02
#define MCP_RTS       0x80
#define MCP_READ_RX   0x90
#define MCP_LOAD_TX   0x40

// MCP2515 Registers
#define MCP_CANSTAT   0x0E
#define MCP_CANCTRL   0x0F

#define MCP_CNF1      0x2A
#define MCP_CNF2      0x29
#define MCP_CNF3      0x28

// TX Registers
#define MCP_TXB0CTRL  0x30
#define MCP_TXB0SIDH  0x31
#define MCP_TXB0SIDL  0x32
#define MCP_TXB0DLC   0x35
#define MCP_TXB0D0    0x36

// RX Registers
#define MCP_RXB0CTRL  0x60
#define MCP_RXB0SIDH  0x61
#define MCP_RXB0SIDL  0x62
#define MCP_RXB0DLC   0x65
#define MCP_RXB0D0    0x66

#define MCP_RXB1CTRL  0x70
#define MCP_RXB1SIDH  0x71
#define MCP_RXB1SIDL  0x72
#define MCP_RXB1DLC   0x75
#define MCP_RXB1D0    0x76

// Interrupt registers
#define MCP_CANINTF   0x2C
#define MCP_CANINTE   0x2B
#define MCP_EFLG      0x2D

// Masks and Filters
#define MCP_RXM0SIDH  0x20
#define MCP_RXM0SIDL  0x21
#define MCP_RXM1SIDH  0x24
#define MCP_RXM1SIDL  0x25

#define MODE_NORMAL 0x00
#define MODE_CONFIG 0x80

extern SPI_HandleTypeDef hspi1;

typedef enum {
    MCP_8MHZ = 0,
} MCP_Clock;

typedef enum {
    CAN_500KBPS = 0,
} CAN_Bitrate;

/* CAN frame struct */
typedef struct {
    uint32_t id;
    uint8_t dlc;
    uint8_t data[8];
} CAN_Frame;

HAL_StatusTypeDef MCP2515_Reset(void);
HAL_StatusTypeDef MCP2515_SetBitrate(CAN_Bitrate bitrate, MCP_Clock clock);
HAL_StatusTypeDef MCP2515_SetNormalMode(void);
HAL_StatusTypeDef MCP2515_SendMessage(CAN_Frame *frame);
HAL_StatusTypeDef MCP2515_ReceiveMessage(CAN_Frame *frame);
HAL_StatusTypeDef MCP2515_Init(void);

// utils
uint8_t MCP2515_ReadByte(uint8_t address);
void MCP2515_WriteByte(uint8_t address, uint8_t data);

#endif /* MCP2515_H_ */

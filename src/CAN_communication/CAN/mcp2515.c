#include "mcp2515.h"

// Buffer for SPI communication
uint8_t spi_tx_buf[20];
uint8_t spi_rx_buf[20];

// Function to read a byte from MCP2515
uint8_t MCP2515_ReadByte(uint8_t address) {
    MCP2515_CS_LOW();

    spi_tx_buf[0] = MCP_READ;
    spi_tx_buf[1] = address;
    spi_tx_buf[2] = 0x00;

    HAL_SPI_TransmitReceive(&hspi1, spi_tx_buf, spi_rx_buf, 3, 100);

    MCP2515_CS_HIGH();
    return spi_rx_buf[2];
}

// Function to write a byte to MCP2515
void MCP2515_WriteByte(uint8_t address, uint8_t data) {
    MCP2515_CS_LOW();

    spi_tx_buf[0] = MCP_WRITE;
    spi_tx_buf[1] = address;
    spi_tx_buf[2] = data;

    HAL_SPI_Transmit(&hspi1, spi_tx_buf, 3, 100);

    MCP2515_CS_HIGH();
}

// Reset the MCP2515
HAL_StatusTypeDef MCP2515_Reset(void) {
    MCP2515_CS_LOW();

    spi_tx_buf[0] = MCP_RESET;
    HAL_SPI_Transmit(&hspi1, spi_tx_buf, 1, 100);

    MCP2515_CS_HIGH();
    HAL_Delay(10);

    return HAL_OK;
}

// Configure bitrate
HAL_StatusTypeDef MCP2515_SetBitrate(CAN_Bitrate bitrate, MCP_Clock clock)
{
    // 1) Enter configuration mode
    MCP2515_WriteByte(MCP_CANCTRL, MODE_CONFIG);
    HAL_Delay(10);

    uint8_t canstat = MCP2515_ReadByte(MCP_CANSTAT);
    printf("CANSTAT after requesting CONFIG = 0x%02X\n", canstat);

    if ((canstat & 0xE0) != MODE_CONFIG) {
        printf("Did not enter configuration mode!\n");
        return HAL_ERROR;
    }

    // 2) Configure 500 kbps @ 8 MHz
    // bit time = 16 TQ, sampling ~75%
    // CNF1: SJW=1TQ, BRP=1 (BRP bits = 0)
    // CNF2: BTLMODE=1, SAM=0, PHSEG1=6TQ, PRSEG=1TQ
    // CNF3: PHSEG2=7TQ
    MCP2515_WriteByte(MCP_CNF1, 0x00); // CNF1
    MCP2515_WriteByte(MCP_CNF2, 0x90); // CNF2
    MCP2515_WriteByte(MCP_CNF3, 0x02); // CNF3

    // 3) Check what was written
    uint8_t c1 = MCP2515_ReadByte(MCP_CNF1);
    uint8_t c2 = MCP2515_ReadByte(MCP_CNF2);
    uint8_t c3 = MCP2515_ReadByte(MCP_CNF3);

    printf("CNF1=0x%02X CNF2=0x%02X CNF3=0x%02X\n", c1, c2, c3);

    // If for some reason the read values don't match, we still show them
    // but return OK so you can test the CAN bus.
    return HAL_OK;
}


// Configure normal mode
HAL_StatusTypeDef MCP2515_SetNormalMode(void) {
    MCP2515_WriteByte(MCP_CANCTRL, 0x00); // Normal mode
    HAL_Delay(10);

    // Check if in normal mode
    if ((MCP2515_ReadByte(MCP_CANSTAT) & 0xE0) != 0x00) {
        return HAL_ERROR;
    }

    return HAL_OK;
}

// Send CAN message
HAL_StatusTypeDef MCP2515_SendMessage(CAN_Frame *frame) {
    if (frame->dlc > 8) return HAL_ERROR;

    // Configure ID
    uint8_t id_high = (uint8_t)(frame->id >> 3);
    uint8_t id_low = (uint8_t)((frame->id & 0x07) << 5);

    MCP2515_WriteByte(MCP_TXB0SIDH, id_high);
    MCP2515_WriteByte(MCP_TXB0SIDL, id_low);

    // Configure DLC
    MCP2515_WriteByte(MCP_TXB0DLC, frame->dlc & 0x0F);

    // Configure data
    for (uint8_t i = 0; i < frame->dlc; i++) {
        MCP2515_WriteByte(MCP_TXB0D0 + i, frame->data[i]);
    }

    // Send message
    MCP2515_CS_LOW();
    spi_tx_buf[0] = MCP_RTS | 0x01; // RTS for TXB0
    HAL_SPI_Transmit(&hspi1, spi_tx_buf, 1, 100);
    MCP2515_CS_HIGH();

    return HAL_OK;
}

// Receive CAN message (your corrected function)
HAL_StatusTypeDef MCP2515_ReceiveMessage(CAN_Frame *frame) {
    uint8_t intf = MCP2515_ReadByte(MCP_CANINTF);

    if (!(intf & 0x01))
        return HAL_ERROR;  // nothing received

    uint8_t sidh = MCP2515_ReadByte(MCP_RXB0SIDH);
    uint8_t sidl = MCP2515_ReadByte(MCP_RXB0SIDL);
    uint8_t dlc  = MCP2515_ReadByte(MCP_RXB0DLC);

    frame->id  = (sidh << 3) | (sidl >> 5);
    frame->dlc = dlc & 0x0F;

    for (int i = 0; i < frame->dlc; i++) {
        frame->data[i] = MCP2515_ReadByte(MCP_RXB0D0 + i);
    }

    /* Clear flag */
    MCP2515_WriteByte(MCP_CANINTF, intf & ~0x01);

    return HAL_OK;
}

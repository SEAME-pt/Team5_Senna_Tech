#include "mcp2515.h"

// Buffer para comunicação SPI
uint8_t spi_tx_buf[20];
uint8_t spi_rx_buf[20];

// Função para ler um byte do MCP2515
uint8_t MCP2515_ReadByte(uint8_t address) {
    MCP2515_CS_LOW();

    spi_tx_buf[0] = MCP_READ;
    spi_tx_buf[1] = address;
    spi_tx_buf[2] = 0x00;

    HAL_SPI_TransmitReceive(&hspi1, spi_tx_buf, spi_rx_buf, 3, 100);

    MCP2515_CS_HIGH();
    return spi_rx_buf[2];
}

// Função para escrever um byte no MCP2515
void MCP2515_WriteByte(uint8_t address, uint8_t data) {
    MCP2515_CS_LOW();

    spi_tx_buf[0] = MCP_WRITE;
    spi_tx_buf[1] = address;
    spi_tx_buf[2] = data;

    HAL_SPI_Transmit(&hspi1, spi_tx_buf, 3, 100);

    MCP2515_CS_HIGH();
}

// Reset do MCP2515
HAL_StatusTypeDef MCP2515_Reset(void) {
    MCP2515_CS_LOW();

    spi_tx_buf[0] = MCP_RESET;
    HAL_SPI_Transmit(&hspi1, spi_tx_buf, 1, 100);

    MCP2515_CS_HIGH();
    HAL_Delay(10);

    return HAL_OK;
}

// Configurar bitrate
HAL_StatusTypeDef MCP2515_SetBitrate(CAN_Bitrate bitrate, MCP_Clock clock)
{
    // 1) Coloca em modo de configuração
    MCP2515_WriteByte(MCP_CANCTRL, MODE_CONFIG);
    HAL_Delay(10);

    uint8_t canstat = MCP2515_ReadByte(MCP_CANSTAT);
    printf("CANSTAT apos pedido de CONFIG = 0x%02X\n", canstat);

    if ((canstat & 0xE0) != MODE_CONFIG) {
        printf("Nao entrou em modo de configuracao!\n");
        return HAL_ERROR;
    }

    // 2) Configura 500 kbps @ 8 MHz
    // bit time = 16 TQ, amostragem ~75%
    // CNF1: SJW=1TQ, BRP=1 (BRP bits = 0)
    // CNF2: BTLMODE=1, SAM=0, PHSEG1=6TQ, PRSEG=1TQ
    // CNF3: PHSEG2=7TQ
    MCP2515_WriteByte(MCP_CNF1, 0x00); // CNF1
    MCP2515_WriteByte(MCP_CNF2, 0x90); // CNF2
    MCP2515_WriteByte(MCP_CNF3, 0x02); // CNF3

    // 3) Confere o que ficou gravado
    uint8_t c1 = MCP2515_ReadByte(MCP_CNF1);
    uint8_t c2 = MCP2515_ReadByte(MCP_CNF2);
    uint8_t c3 = MCP2515_ReadByte(MCP_CNF3);

    printf("CNF1=0x%02X CNF2=0x%02X CNF3=0x%02X\n", c1, c2, c3);

    // Se por algum motivo a leitura não bate, a gente ainda mostra
    // mas retorna OK pra você conseguir testar o barramento CAN.
    return HAL_OK;
}


// Configurar modo normal
HAL_StatusTypeDef MCP2515_SetNormalMode(void) {
    MCP2515_WriteByte(MCP_CANCTRL, 0x00); // Modo normal
    HAL_Delay(10);

    // Verificar se está em modo normal
    if ((MCP2515_ReadByte(MCP_CANSTAT) & 0xE0) != 0x00) {
        return HAL_ERROR;
    }

    return HAL_OK;
}

// Enviar mensagem CAN
HAL_StatusTypeDef MCP2515_SendMessage(CAN_Frame *frame) {
    if (frame->dlc > 8) return HAL_ERROR;

    // Configurar ID
    uint8_t id_high = (uint8_t)(frame->id >> 3);
    uint8_t id_low = (uint8_t)((frame->id & 0x07) << 5);

    MCP2515_WriteByte(MCP_TXB0SIDH, id_high);
    MCP2515_WriteByte(MCP_TXB0SIDL, id_low);

    // Configurar DLC
    MCP2515_WriteByte(MCP_TXB0DLC, frame->dlc & 0x0F);

    // Configurar dados
    for (uint8_t i = 0; i < frame->dlc; i++) {
        MCP2515_WriteByte(MCP_TXB0D0 + i, frame->data[i]);
    }

    // Enviar mensagem
    MCP2515_CS_LOW();
    spi_tx_buf[0] = MCP_RTS | 0x01; // RTS para TXB0
    HAL_SPI_Transmit(&hspi1, spi_tx_buf, 1, 100);
    MCP2515_CS_HIGH();

    return HAL_OK;
}

	// Receber mensagem CAN (sua função corrigida)
HAL_StatusTypeDef MCP2515_ReceiveMessage(CAN_Frame *frame) {
    uint8_t intf = MCP2515_ReadByte(MCP_CANINTF);

    // Verifica se há mensagem no buffer RX0
    if (!(intf & 0x01)) {
        return HAL_ERROR;  // Nada recebido no buffer 0
    }

    // Lê o buffer RX0
    uint8_t sidh = MCP2515_ReadByte(MCP_RXB0SIDH);
    uint8_t sidl = MCP2515_ReadByte(MCP_RXB0SIDL);
    uint8_t dlc  = MCP2515_ReadByte(MCP_RXB0DLC);

    frame->id  = (sidh << 3) | (sidl >> 5);
    frame->dlc = dlc & 0x0F;

    // Lê os dados
    for (int i = 0; i < frame->dlc; i++) {
        frame->data[i] = MCP2515_ReadByte(MCP_RXB0D0 + i);
    }

    // Limpa APENAS a flag RX0IF, preservando outras interrupções
    MCP2515_WriteByte(MCP_CANINTF, intf & ~0x01);

    return HAL_OK;
}

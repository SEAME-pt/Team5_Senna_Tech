#ifndef SRF08_H
#define SRF08_H

#include "utils.h"
#include "i2c.h"

#define SRF08_DEFAULT_ADDR      0xE0  // 8-bit address (shifted: 0x70 << 1)
#define SRF08_CMD_RANGE_CM      0x51  // Ranging Mode - Result in centimeters
#define SRF08_REG_CMD           0x00  // Set Maximum Analogue Gain to 94
#define SRF08_REG_RANGE_HIGH    0x02  // high byte of first echo
#define SRF08_REG_RANGE_LOW     0x03  // low byte of first echo

// SRF08 requires ~65ms after trigger before the result is ready
#define SRF08_RANGING_DELAY_MS  70

#endif

UINT    srf08_init(UINT addr);
ULONG   srf08_read_cm(UINT addr, ULONG *distance_cm);

// very useful documentation: https://www.robot-electronics.co.uk/htm/srf08tech.html

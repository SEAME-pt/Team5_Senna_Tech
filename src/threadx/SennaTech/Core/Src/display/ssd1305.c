#include "ssd1305.h"

static uint8_t g_buffer[SSD1305_BUF_SIZE];

static void oled_delay_ms(uint32_t ms)
{
    tx_thread_sleep(ms);
}

static void oled_cs_low(void)
{
    HAL_GPIO_WritePin(GPIOG, GPIO_PIN_12, GPIO_PIN_RESET);
}

static void oled_cs_high(void)
{
    HAL_GPIO_WritePin(GPIOG, GPIO_PIN_12, GPIO_PIN_SET);
}

static void oled_dc_cmd(void)
{
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_12, GPIO_PIN_RESET);
}

static void oled_dc_data(void)
{
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_12, GPIO_PIN_SET);
}

static void oled_rst_low(void)
{
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_13, GPIO_PIN_RESET);
}

static void oled_rst_high(void)
{
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_13, GPIO_PIN_SET);
}

static void ssd1305_write_cmd(uint8_t cmd)
{
    oled_cs_low();
    oled_dc_cmd();
    HAL_SPI_Transmit(&hspi3, &cmd, 1, HAL_MAX_DELAY);
    oled_cs_high();
}

static void ssd1305_write_data(uint8_t *data, uint16_t len)
{
    oled_cs_low();
    oled_dc_data();
    HAL_SPI_Transmit(&hspi3, data, len, HAL_MAX_DELAY);
    oled_cs_high();
}

static void ssd1305_reset(void)
{
    oled_rst_high();
    oled_delay_ms(10);
    oled_rst_low();
    oled_delay_ms(10);
    oled_rst_high();
    oled_delay_ms(100);
}

void ssd1305_init()
{
    /* CS -> PG12, DC -> PC12, RST -> PB13 */
    HAL_GPIO_WritePin(GPIOG, GPIO_PIN_12, GPIO_PIN_SET);
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_12, GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_13, GPIO_PIN_SET);

    ssd1305_reset();

    ssd1305_write_cmd(0xAE); // Display off

    ssd1305_write_cmd(0xD5); // Set display clock divide ratio
    ssd1305_write_cmd(0x80);

    ssd1305_write_cmd(0xA8); // Multiplex ratio
    ssd1305_write_cmd(0x1F); // 32MUX

    ssd1305_write_cmd(0xD3); // Display offset
    ssd1305_write_cmd(0x00);

    ssd1305_write_cmd(0x40); // Display start line

    ssd1305_write_cmd(0x8D); // Charge pump
    ssd1305_write_cmd(0x14);

    ssd1305_write_cmd(0x20); // Memory addressing mode
    ssd1305_write_cmd(0x00); // Horizontal addressing mode

    ssd1305_write_cmd(0xA1); // Segment remap
    ssd1305_write_cmd(0xC8); // COM scan direction remapped

    ssd1305_write_cmd(0xDA); // COM pins hardware config
    ssd1305_write_cmd(0x02);

    ssd1305_write_cmd(0x81); // Contrast
    ssd1305_write_cmd(0x8F);

    ssd1305_write_cmd(0xD9); // Pre-charge period
    ssd1305_write_cmd(0xF1);

    ssd1305_write_cmd(0xDB); // VCOMH deselect level
    ssd1305_write_cmd(0x40);

    ssd1305_write_cmd(0xA4); // Resume RAM display
    ssd1305_write_cmd(0xA6); // Normal display

    ssd1305_clear();
    ssd1305_update();

    ssd1305_write_cmd(0xAF); // Display on
}

void ssd1305_clear(void)
{
    ssd1305_fill(0x00);
}

void ssd1305_fill(uint8_t value)
{
    uint16_t i;

    i = 0;
    while (i < SSD1305_BUF_SIZE)
    {
        g_buffer[i] = value;
        i++;
    }
}

void ssd1305_update(void)
{
    uint8_t page = 0;

    while (page < SSD1305_PAGES)
    {
        ssd1305_write_cmd(0xB0 + page);
        ssd1305_write_cmd(0x00);
        ssd1305_write_cmd(0x10);

        ssd1305_write_data(&g_buffer[SSD1305_WIDTH * page], SSD1305_WIDTH);

        page++;
    }
}

void ssd1305_draw_pixel(uint8_t x, uint8_t y, uint8_t color)
{
    uint16_t    index;
    uint8_t     bit;

    if (x >= SSD1305_WIDTH || y >= SSD1305_HEIGHT)
        return ;

    index = x + (y / 8) * SSD1305_WIDTH;
    bit = 1 << (y % 8);

    if (color)
        g_buffer[index] |= bit;
    else
        g_buffer[index] &= ~bit;
}

void ssd1305_draw_line(uint8_t x, uint8_t y,
        uint8_t len, uint8_t color)
{
    uint8_t i;

    i = 0;
    while (i < len)
    {
        ssd1305_draw_pixel(x + i, y, color);
        i++;
    }
}

void ssd1305_fill_ellipse(uint8_t cx, uint8_t cy,
        uint8_t rx, uint8_t ry, uint8_t color)
{
    int16_t x;
    int16_t y;
    int32_t dx;
    int32_t dy;
    int32_t limit;

    y = -ry;
    limit = (int32_t)rx * rx * ry * ry;
    while (y <= ry)
    {
        x = -rx;
        while (x <= rx)
        {
            dx = (int32_t)x * x * ry * ry;
            dy = (int32_t)y * y * rx * rx;
            if (dx + dy <= limit)
                ssd1305_draw_pixel(cx + x, cy + y, color);
            x++;
        }
        y++;
    }
}
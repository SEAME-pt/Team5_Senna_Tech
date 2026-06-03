#include "ssd1305.h"

static void ssd1305_draw_thick_hline(uint8_t x, uint8_t y,
        uint8_t len, uint8_t color)
{
    ssd1305_draw_line(x, y, len, color);
    ssd1305_draw_line(x, y + 1, len, color);
    ssd1305_draw_line(x, y - 1, len, color);
}

static void ssd1305_draw_z(uint8_t x, uint8_t y, uint8_t size)
{
    uint8_t i;

    ssd1305_draw_line(x, y, size, 1);
    ssd1305_draw_line(x, y + 1, size, 1);

    i = 0;
    while (i < size)
    {
        ssd1305_draw_pixel(x + size - 1 - i, y + 2 + (i / 2), 1);
        ssd1305_draw_pixel(x + size - i, y + 2 + (i / 2), 1);
        i++;
    }

    ssd1305_draw_line(x, y + 7, size, 1);
    ssd1305_draw_line(x, y + 8, size, 1);
}

void ssd1305_draw_sleep_face(uint8_t frame)
{
    uint8_t phase;

    phase = frame % 4;
    ssd1305_clear();

    /* Eyes */
    ssd1305_draw_thick_hline(30, 20, 28, 1);
    ssd1305_draw_thick_hline(70, 20, 28, 1);

    /*
     * Z animation inverted for your OLED orientation:
     * each next Z moves visually UP.
     */
    if (phase == 0)
    {
        ssd1305_draw_z(104, 14, 8);
    }
    else if (phase == 1)
    {
        ssd1305_draw_z(104, 14, 8);
        ssd1305_draw_z(114, 18, 7);
    }
    else if (phase == 2)
    {
        ssd1305_draw_z(104, 14, 8);
        ssd1305_draw_z(114, 18, 7);
        ssd1305_draw_z(122, 22, 6);
    }
    else
    {
        ssd1305_draw_z(114, 18, 7);
        ssd1305_draw_z(122, 22, 6);
    }

    ssd1305_update();
}
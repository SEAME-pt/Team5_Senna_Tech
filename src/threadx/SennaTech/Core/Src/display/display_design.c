#include "ssd1305.h"

static void ssd1305_fill_ellipse(uint8_t cx, uint8_t cy,
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

void ssd1305_draw_headlights(void)
{
    ssd1305_clear();

    ssd1305_fill_ellipse(34, 16, 18, 10, 1);
    ssd1305_fill_ellipse(94, 16, 18, 10, 1);

    ssd1305_fill_ellipse(34, 16, 9, 4, 0);
    ssd1305_fill_ellipse(94, 16, 9, 4, 0);

    ssd1305_draw_line(19, 16, 30, 1);
    ssd1305_draw_line(79, 16, 30, 1);

    ssd1305_fill_ellipse(34, 16, 5, 2, 1);
    ssd1305_fill_ellipse(94, 16, 5, 2, 1);

    ssd1305_update();
}

void ssd1305_draw_cute_eyes(void)
{
    ssd1305_clear();

    /* Left eye */
    ssd1305_fill_ellipse(38, 16, 18, 13, 1);
    ssd1305_fill_ellipse(42, 18, 8, 8, 0);
    ssd1305_fill_ellipse(38, 13, 3, 3, 1);
    ssd1305_fill_ellipse(45, 22, 2, 2, 1);

    /* Right eye */
    ssd1305_fill_ellipse(90, 16, 18, 13, 1);
    ssd1305_fill_ellipse(86, 18, 8, 8, 0);
    ssd1305_fill_ellipse(82, 13, 3, 3, 1);
    ssd1305_fill_ellipse(89, 22, 2, 2, 1);

    /* Small cute upper eyelid effect */
    ssd1305_fill_ellipse(38, 7, 16, 4, 0);
    ssd1305_fill_ellipse(90, 7, 16, 4, 0);

    ssd1305_update();
}

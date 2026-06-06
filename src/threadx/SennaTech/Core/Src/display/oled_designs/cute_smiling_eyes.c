#include "ssd1305.h"

static void ssd1305_draw_dot_2x2(UINT x, UINT y, UINT color)
{
    ssd1305_draw_pixel(x, y, color);
    ssd1305_draw_pixel(x + 1, y, color);
    ssd1305_draw_pixel(x, y + 1, color);
    ssd1305_draw_pixel(x + 1, y + 1, color);
}

static void ssd1305_draw_happy_eye_up(UINT cx, int8_t bounce)
{
    UINT i;
    UINT x;
    UINT y;

    i = 0;
    while (i <= 14)
    {
        x = cx - 14 + i;
        y = 17 + (i / 2) + bounce;
        ssd1305_draw_dot_2x2(x, y, 1);
        i++;
    }

    i = 0;
    while (i <= 14)
    {
        x = cx + i;
        y = 24 - (i / 2) + bounce;
        ssd1305_draw_dot_2x2(x, y, 1);
        i++;
    }
}

void ssd1305_draw_happy_eyes(UINT frame)
{
    int8_t bounce;

    bounce = 0;
    if ((frame % 8) == 1 || (frame % 8) == 2)
        bounce = -1;
    if ((frame % 8) == 5 || (frame % 8) == 6)
        bounce = 1;

    ssd1305_clear();

    ssd1305_draw_happy_eye_up(38, bounce);
    ssd1305_draw_happy_eye_up(90, bounce);

    ssd1305_update();
}

#include "ssd1305.h"

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

void ssd1305_draw_half_closed_eyes(void)
{
    ssd1305_clear();

    /* Left half-closed eye */
    ssd1305_fill_ellipse(38, 18, 18, 7, 1);
    ssd1305_fill_ellipse(42, 19, 7, 5, 0);
    ssd1305_fill_ellipse(38, 16, 3, 2, 1);

    /* Right half-closed eye */
    ssd1305_fill_ellipse(90, 18, 18, 7, 1);
    ssd1305_fill_ellipse(86, 19, 7, 5, 0);
    ssd1305_fill_ellipse(82, 16, 3, 2, 1);

    /* Eyelid cover */
    ssd1305_fill_ellipse(38, 10, 18, 7, 0);
    ssd1305_fill_ellipse(90, 10, 18, 7, 0);

    ssd1305_update();
}

void ssd1305_draw_closed_eyes(void)
{
    ssd1305_clear();

    /* Left closed eye */
    ssd1305_draw_line(22, 16, 32, 1);
    ssd1305_draw_line(23, 17, 30, 1);
    ssd1305_draw_line(24, 18, 28, 1);

    /* Right closed eye */
    ssd1305_draw_line(74, 16, 32, 1);
    ssd1305_draw_line(75, 17, 30, 1);
    ssd1305_draw_line(76, 18, 28, 1);

    ssd1305_update();
}
#include "ssd1305.h"

void oled_thread_entry(ULONG thread_input)
{
    ssd1305_init();

    ssd1305_draw_cute_eyes();

    while (1)
    {
        tx_thread_sleep(1000);
    }
}

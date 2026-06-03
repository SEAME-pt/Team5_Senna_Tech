#include "ssd1305.h"

void oled_thread_entry(ULONG thread_input)
{
    uint8_t smile_cycle;
    uint8_t frame;

    (void)thread_input;

    smile_cycle = 0;
    frame = 0;

    ssd1305_init();

    while (1)
    {
        ssd1305_draw_cute_eyes();

        tx_thread_sleep(9 * TX_TIMER_TICKS_PER_SECOND);

        ssd1305_draw_half_closed_eyes();
        tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND / 12);

        ssd1305_draw_closed_eyes();
        tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND / 8);

        ssd1305_draw_half_closed_eyes();
        tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND / 12);

        smile_cycle++;

        if (smile_cycle >= 4)
        {
            smile_cycle = 0;
            frame = 0;

            while (frame < 12)
            {
                ssd1305_draw_happy_eyes(frame);
                tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND / 4);
                frame++;
            }
        }

        ssd1305_draw_cute_eyes();
    }
}

/* void oled_thread_entry(ULONG thread_input)
{
    uint8_t frame;

    (void)thread_input;

    frame = 0;
    ssd1305_init();

    while (1)
    {
        ssd1305_draw_sleep_face(frame);
        frame++;
        tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND / 2);
    }
} */
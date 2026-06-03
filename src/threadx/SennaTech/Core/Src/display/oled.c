#include "ssd1305.h"
#include "ultrasonic.h"

static UINT oled_read_ultrasonic(t_ultrasonic_data *ultrasonic_data)
{
    if (tx_queue_receive(&g_ultrasonic_data_queue,
            ultrasonic_data, TX_NO_WAIT) == TX_SUCCESS)
        return (TX_SUCCESS);
    return (TX_NOT_AVAILABLE);
}

static UINT oled_front_is_close(t_ultrasonic_data *ultrasonic_data)
{
    oled_read_ultrasonic(ultrasonic_data);

    if (ultrasonic_data->front_distance_cm > 0
        && ultrasonic_data->front_distance_cm <= 5)
        return (1);
    return (0);
}

void oled_thread_entry(ULONG thread_input)
{
    uint8_t             frame = 0;
    uint32_t            blink_timer = 0;
    t_ultrasonic_data   ultrasonic_data;
    bzero(&ultrasonic_data, sizeof(ultrasonic_data));

    ssd1305_init();
    ssd1305_draw_cute_eyes();
    uart_send("OLED Thread Entry\r\n");

    while (1)
    {
        if (oled_front_is_close(&ultrasonic_data))
        {
            ssd1305_draw_happy_eyes(frame);
            frame++;
            tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND / 4);
            blink_timer = 0;
        }
        else
        {
            frame = 0;
            ssd1305_draw_cute_eyes();

            tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND / 4);
            blink_timer += TX_TIMER_TICKS_PER_SECOND / 4;

            if (blink_timer >= 10 * TX_TIMER_TICKS_PER_SECOND)
            {
                blink_timer = 0;

                ssd1305_draw_half_closed_eyes();
                tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND / 12);

                ssd1305_draw_closed_eyes();
                tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND / 8);

                ssd1305_draw_half_closed_eyes();
                tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND / 12);

                ssd1305_draw_cute_eyes();
            }
        }
    }
}

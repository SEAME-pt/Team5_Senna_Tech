#include "sleep_hal.h"
#include "app_threadx.h"

void tx_sleep(int timer_ticks)
{
    tx_thread_sleep(timer_ticks);
}

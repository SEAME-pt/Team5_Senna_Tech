#include "can_manager.h"
#include <stdio.h>
#include <inttypes.h>

void log_debug(const char *fmt, ...)
{
    va_list args;
    va_start(args, fmt);

    log_msg_t log;
    vsnprintf(log.msg, sizeof(log.msg), fmt, args);

    va_end(args);

    tx_queue_send(&g_log_queue, &log, TX_NO_WAIT);
}

void debug_thread_entry(ULONG thread_input)
{
    log_msg_t log;

    while (1)
    {
        if (tx_queue_receive(&g_log_queue, &log, TX_WAIT_FOREVER) == TX_SUCCESS)
        {
            printf("%s\n", log.msg);
        }
        tx_thread_sleep(1);
    }
}
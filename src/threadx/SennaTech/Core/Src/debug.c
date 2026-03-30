#include "can_manager.h"
#include <inttypes.h>

void debug_thread_entry(ULONG thread_input)
{
    log_msg_t log;

    while (1)
    {
        /* if (tx_queue_receive(&g_log_queue, &log, TX_WAIT_FOREVER) == TX_SUCCESS)
        {
            printf("%s\n", log.msg);
        }
        tx_thread_sleep(1); */
    }
}
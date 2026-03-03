#include "can_manager.h"

void heartbeat_thread_entry(ULONG thread_input)
{
    CAN_Frame hb_frame;
    hb_frame.id = CAN_ID_HEARTBEAT;
    hb_frame.dlc = 1;
    hb_frame.data[0] = 0xAA;

    uart_send("HEARTBEAT THREAD STARTED\r\n");

    while(1)
    {
        tx_queue_send(&g_tx_data_queue, &hb_frame, TX_NO_WAIT);

        tx_thread_sleep(100);
    }
}

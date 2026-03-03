#include "can_manager.h"
#include <stdio.h>
#include "car.h"
#include <inttypes.h>

float percent_from_can_int16(uint8_t low_byte, uint8_t high_byte)
{
    // Intel (little endian)
    uint16_t u_combined = ((uint16_t)high_byte << 8) | low_byte;

    int16_t raw = (int16_t)u_combined;

    float percent = raw * 0.01f;

    // safety clamp
    if (percent > 1.0f)  percent = 1.0f;
    if (percent < -1.0f) percent = -1.0f;

    return percent;
}

void motors_thread_entry(ULONG thread_input)
{
    uart_send("Motor Thread Entry\r\n");

    CAN_Frame frame;

    car_t car;
    car_init(&car, &hi2c1);


    while (1)
    {
        tx_queue_receive(&g_rx_data_queue, &frame, TX_WAIT_FOREVER);

        if (frame.dlc < 2) continue; // segurança: precisamos de 2 bytes

        float percent = percent_from_can_int16(frame.data[0], frame.data[1]);

/*         log_debug(
            "[RX] ID: 0x%lX | bytes: %02X %02X | percent: %.3f",
            frame.id,
            frame.data[0],
            frame.data[1],
            percent
        ); */

        if (frame.id == CAN_ID_MOTOR_CMD)
        {
            car_set_throttle_percent(&car, percent);
        }
        else if (frame.id == CAN_ID_STEER_CMD)
        {
            car_set_steering_percent(&car, percent);
        }
    }

    uart_send("Car test finished!\r\n");
}

#include "can_manager.h"
#include <stdio.h>
#include "car.h"
#include <inttypes.h>

float percent_from_can_int16(uint8_t high_byte, uint8_t low_byte)
{
    // 1. Monta o valor em uma variável de 16 bits sem sinal primeiro
    uint16_t u_combined = ((uint16_t)high_byte << 8) | (uint16_t)low_byte;

    // 2. Converte para inteiro com sinal (o hardware faz isso via complemento de 2)
    int16_t raw = (int16_t)u_combined;

    // 3. Converte para float e normaliza
    float percent = (float)raw / 32767.0f;

    // 4. Clamp de segurança para evitar que -32768 (limite do int16) saia do range -1.0 a 1.0
    if (percent > 1.0f)  percent = 1.0f;
    if (percent < -1.0f) percent = -1.0f;

    return percent;
}

void motors_thread_entry(ULONG thread_input)
{
    printf("Motor Thread Entry");

    CAN_Frame frame;

    car_t car;
    car_init(&car, &hi2c1);

    // TESTE ADDRESSES
/*     for (uint8_t addr = 1; addr < 127; addr++)
    {
        if (HAL_I2C_IsDeviceReady(&hi2c1, addr << 1, 1, 10) == HAL_OK)
        {
            printf("I2C device found at 0x%02X\n", addr);
        }
    } */

    while (1)
    {
        tx_queue_receive(&g_rx_data_queue, &frame, TX_WAIT_FOREVER);

        if (frame.dlc < 2) continue; // segurança: precisamos de 2 bytes

        float percent = percent_from_can_int16(frame.data[0], frame.data[1]);

        printf(
            "[RX] ID: 0x%lX | bytes: %02X %02X | percent: %.3f\n",
            frame.id,
            frame.data[0],
            frame.data[1],
            percent
        );

        if (frame.id == CAN_ID_MOTOR_CMD)
        {
            car_set_throttle_percent(&car, percent);
        }
        else if (frame.id == CAN_ID_STEER_CMD)
        {
            car_set_steering_percent(&car, percent);
        }
    }
        

    /* Teste steering */
/*     car_set_steering_percent(&car, 0.0f);
    tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND);

    car_set_steering_percent(&car, 0.5f);
    tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND);

    car_set_steering_percent(&car, -0.5f);
    tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND); */
    //car_set_throttle_percent(&car, 0.2f);
    /* Teste throttle */
/*     car_set_throttle_percent(&car, 0.5f); // frente
    tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND * 2);

    car_set_throttle_percent(&car, -0.5f); // ré
    tx_thread_sleep(TX_TIMER_TICKS_PER_SECOND * 2);

    car_set_throttle_percent(&car, 0.0f); // parar */

    printf("Car test finished!\n");
    printf("Motor thread encerrou!");
}

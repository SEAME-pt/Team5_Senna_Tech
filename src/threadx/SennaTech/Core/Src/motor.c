#include "can_manager.h"
#include <stdio.h>
#include "car.h"

void motors_thread_entry(ULONG thread_input)
{
    printf("Motor Thread Entry");

    for (uint8_t addr = 1; addr < 127; addr++)
    {
        if (HAL_I2C_IsDeviceReady(&hi2c1, addr << 1, 1, 10) == HAL_OK)
        {
            printf("I2C device found at 0x%02X\n", addr);
        }
    }
    
    car_t car;

    car_init(&car, &hi2c1);

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

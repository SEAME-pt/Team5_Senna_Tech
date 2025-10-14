from jetracer.nvidia_racecar import NvidiaRacecar
import pygame
import time
#coment
car = NvidiaRacecar()

pygame.init()
pygame.joystick.init()

# Verifica se há joystick disponível
if pygame.joystick.get_count() == 0:
    print("Nenhum joystick conectado!")
    exit(1)

joystick = pygame.joystick.Joystick(0)
joystick.init()

car.throttle_gain = 1
car.steering_gain = 1  # Definindo o steering_gain explicitamente
car.steering_offset = 0

try:
    while True:
        pygame.event.pump()

        throttle_axis = joystick.get_axis(1)
        steering_axis = joystick.get_axis(2)

        # Ajustando o throttle (normalmente, eixo 1 de joystick vai de -1 (up) a 1 (down), então inverte se necessário)
        car.throttle = throttle_axis * car.throttle_gain

        # Ajustando o steering
        car.steering = steering_axis * car.steering_gain

        print(f"Throttle: {car.throttle:.2f}, Steering: {car.steering:.2f}")

        time.sleep(0.05)  # Coloquei o sleep dentro do loop para não sobrecarregar o CPU

except KeyboardInterrupt:
    print("\nSaindo...")

finally:
    car.throttle = 0
    car.steering = 0
    pygame.joystick.quit()
    pygame.quit()

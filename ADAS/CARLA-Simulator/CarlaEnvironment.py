import carla
import random

class CarlaEnvironment:

    def __init__(self):
        self.client = carla.Client("localhost", 2000)
        self.client.set_timeout(10.0)

        #print(self.client.get_available_maps())

        # Carrega mundo
        self.world = self.client.load_world(
            'Town04_Opt',
            carla.MapLayer.Buildings |
            carla.MapLayer.ParkedVehicles |
            carla.MapLayer.Foliage |
            carla.MapLayer.Decals |
            carla.MapLayer.Particles
        )

        self.world.unload_map_layer(carla.MapLayer.Buildings)
        self.world.unload_map_layer(carla.MapLayer.ParkedVehicles)
        self.world.unload_map_layer(carla.MapLayer.Foliage)
        self.world.unload_map_layer(carla.MapLayer.Decals)
        self.world.unload_map_layer(carla.MapLayer.Particles)

        # Traffic Manager
        self.traffic_manager = self.client.get_trafficmanager(8000)

        # Configuração de modo síncrono
        settings = self.world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        self.world.apply_settings(settings)

        self.traffic_manager.set_synchronous_mode(True)

        # Blueprints e spawn points
        self.blueprint_lib = self.world.get_blueprint_library()
        self.spawn_points = self.world.get_map().get_spawn_points()

        # Controle do clima
        self.weather_time = 0.0
        self.weather_delta = settings.fixed_delta_seconds
        self.traffic_actors = []

    def update_weather(self):
        """
        Atualiza o clima dinamicamente.
        Sempre dia, sem chuva, com variação rápida de nuvens e neblina.
        """
        # Atualiza o tempo interno
        self.weather_time += self.weather_delta

        # Cloudiness (20 a 60%) e fog_density (5 a 25%) aleatório por tick
        cloudiness = random.uniform(0, 60)
        fog_density = random.uniform(0, 25)

        # Sun altitude fixo alto para evitar noite (50 a 70 graus)
        sun_altitude = random.uniform(20, 90)

        # Sun azimuth levemente aleatório, apenas para variar posição do sol
        sun_azimuth = random.uniform(150, 210)

        weather = carla.WeatherParameters(
            cloudiness=cloudiness,
            precipitation=0.0,
            precipitation_deposits=0.0,
            fog_density=fog_density,
            wetness=0.0,
            sun_altitude_angle=sun_altitude,
            sun_azimuth_angle=sun_azimuth
        )

        self.world.set_weather(weather)

    def create_traffic(self):
        vehicle_bp = self.blueprint_lib.filter("vehicle.*")
        for i in range(20):

            spawn = random.choice(self.spawn_points)

            vehicle = self.world.try_spawn_actor(
                random.choice(vehicle_bp),
                spawn
            )

            if vehicle:
                vehicle.set_autopilot(True, self.traffic_manager.get_port())
                self.traffic_actors.append(vehicle)
import carla
import numpy as np
import cv2

IMG_HEIGHT = 360
IMG_WIDTH = 640

class Vehicle:

    def __init__(self, env, image_queue, image_queue_seg, pid):

        self.env = env
        self.image_queue = image_queue
        self.image_queue_seg = image_queue_seg

        self.actors_list = []

        self.vehicle_actor = None
        self.camera_actor = None
        self.camera_actor_seg = None

        self.setup_vehicle()
        self.setup_sensors()

    def process_image(self, image):

        i = np.frombuffer(image.raw_data, dtype=np.uint8)
        i2 = i.reshape((IMG_HEIGHT, IMG_WIDTH, 4))

        bgr = i2[:, :, :3]
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        frame_id = image.frame

        #by discommenting this, the system will generate rgb images for datasets
        #cv2.imwrite(f"dataset/images/{frame_id}.png", bgr)

        self.image_queue.put((bgr, rgb))

    def process_image_seg(self, image):

        # image.convert(carla.ColorConverter.CityScapesPalette)

        i = np.frombuffer(image.raw_data, dtype=np.uint8)
        i2 = i.reshape((IMG_HEIGHT, IMG_WIDTH, 4))

        seg = i2[:, :, :3]

        frame_id = image.frame

        lane_mask = seg[:,:,2] == 24
        lane_mask_img = lane_mask.astype(np.uint8) * 255
        
        #by discommenting this, the system will generate the lane masks for datasets
        #cv2.imwrite(f"dataset/masks/{frame_id}.png", lane_mask_img)

        self.image_queue_seg.put(seg)

    def setup_vehicle(self):

        vehicle_bp = self.env.blueprint_lib.filter("vehicle.audi.tt")[0]
        vehicle_bp.set_attribute('color', '50, 205, 50')

        self.vehicle_actor = self.env.world.spawn_actor(
            vehicle_bp,
            self.env.spawn_points[1]
        )

        # Autopilot 
        self.vehicle_actor.set_autopilot(False)

        self.actors_list.append(self.vehicle_actor)

    def setup_sensors(self):

        camera_bp = self.env.blueprint_lib.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', str(IMG_WIDTH))
        camera_bp.set_attribute('image_size_y', str(IMG_HEIGHT))
        camera_bp.set_attribute('fov', '102')

        camera_spawn_point = carla.Transform(
            carla.Location(x=1.5, z=1.7),
            carla.Rotation(pitch=-5)
        )

        camera_seg = self.env.blueprint_lib.find('sensor.camera.semantic_segmentation')
        camera_seg.set_attribute('image_size_x', str(IMG_WIDTH))
        camera_seg.set_attribute('image_size_y', str(IMG_HEIGHT))
        camera_seg.set_attribute('fov', '102')

        camera_spawn_point_seg = carla.Transform(
            carla.Location(x=1.5, z=1.7),
            carla.Rotation(pitch=-5)
        )

        self.camera_actor = self.env.world.spawn_actor(
            camera_bp,
            camera_spawn_point,
            attach_to=self.vehicle_actor
        )

        self.camera_actor_seg = self.env.world.spawn_actor(
            camera_seg,
            camera_spawn_point_seg,
            attach_to=self.vehicle_actor
        )

        self.camera_actor.listen(self.process_image)
        self.camera_actor_seg.listen(self.process_image_seg)

        self.actors_list.append(self.camera_actor)
        self.actors_list.append(self.camera_actor_seg)

    def destroy(self):
        if self.camera_actor is not None:
            self.camera_actor.stop()
        if self.camera_actor_seg is not None:
            self.camera_actor_seg.stop()
        for actor in self.actors_list:
            actor.destroy()

    def pid_control_for_steering(self, cte, pid, annotated):
        if cte is not None:

            steering = pid.update(
                target=0.0,     # queremos estar no centro
                current=cte,    # erro atual
                dt=0.05
            )
        else:
            steering = 0.0
        control = carla.VehicleControl(
        throttle=0.5,
        steer=float(steering),
        brake=0.0
        )

        self.vehicle_actor.apply_control(control)
        cv2.putText(
            annotated,
            f"Steer: {steering:.2f}",
            (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,0),
            2
        )
        
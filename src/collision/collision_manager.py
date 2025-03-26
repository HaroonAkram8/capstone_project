from src.collision.environment import Environment
from src.vision.locate import sim_locate, irl_locate

class CollisionManager:
    def __init__(self, simulation: bool=True, cube_length: int=1, camera_intrinsics=None, max_x: int=100, max_y: int=100, max_z: int=10):
        self.cube_length = cube_length
        self.camera_intrinsics = camera_intrinsics

        self.locate = sim_locate
        if not simulation:
            self.locate = irl_locate
        
        self.env = Environment(max_x=max_x, max_y=max_y, max_z=max_z)
    
    def set_camera_intrinsics(self, camera_intrinsics):
        self.camera_intrinsics = camera_intrinsics
    
    def update_state(self, depth_data, curr_pos):
        for img_x in range(640):
            for img_y in range(480):
                location = self.locate(depth_data=depth_data, camera_intrinsics=self.camera_intrinsics, x_centre=img_x, y_centre=img_y, curr_pos=curr_pos)
                
                if location is None:
                    continue

                x = round(location['x'])
                y = round(location['y'])
                z = round(location['z'])

                if z < 1:
                    continue

                self.env.set(val=1, x=x, y=y, z=z)

        # print(self.env.map)



if __name__ == "__main__":
    from src.compiler.converter.drone_api import DroneAPI
    import numpy as np
    np.set_printoptions(threshold=np.inf)

    drone = DroneAPI()

    _, depth_img = drone.get_image()
    curr_pos = drone.current_position()
    camera_intrinsics = drone.get_camera_intrinsics()

    collision_manager = CollisionManager(camera_intrinsics=camera_intrinsics, max_x=10, max_y=10, max_z=3)

    import time
    start_time = time.time()
    collision_manager.update_state(depth_data=depth_img, curr_pos=curr_pos)
    print("--- %s seconds ---" % (time.time() - start_time))

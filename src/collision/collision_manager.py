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
        self.neighbors = [(0, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]
    
    def collision_visuals(self, current_position):
        self.env.visualize(current_position=current_position)

    def set_camera_intrinsics(self, camera_intrinsics):
        self.camera_intrinsics = camera_intrinsics

    def get_path(self, start_pos: tuple, end_pos: tuple):
        return self.env.get_path(start_pos=start_pos, end_pos=end_pos)
    
    def update_state(self, depth_data, curr_pos):
        new_obstacles = {}

        for img_x in range(0, 640, 10):
            for img_y in range(0, 480, 10):
                location, is_max = self.locate(depth_data=depth_data, camera_intrinsics=self.camera_intrinsics, x_centre=img_x, y_centre=img_y, curr_pos=curr_pos)

                if location is None:
                    continue

                x = int(round(location['x']))
                y = int(round(location['y']))
                z = int(round(location['z']))

                if z > -1:
                    continue
                
                if not is_max:
                    for dx, dy, dz in self.neighbors:
                        new_x = x + dx
                        new_y = y + dy
                        new_z = z + dz

                        if (new_x, new_y, new_z) in new_obstacles:
                            continue
                        
                        self.env.set(val=1, x=new_x, y=new_y, z=new_z)
                        new_obstacles[(new_x, new_y, new_z)] = 1
                
                # self._clear_protocol(curr_pos=curr_pos, new_obstacles=new_obstacles, x=x, y=y, z=z)

    def _clear_protocol(self, curr_pos, new_obstacles, x: int, y: int, z: int):
        z1, y1, x1 = self.env.real_to_env(x=x, y=y, z=z)
        z2, y2, x2 = self.env.real_to_env(x=curr_pos["x"], y=curr_pos["y"], z=curr_pos["z"])

        points = self._bresenham_3d(x1=x1, y1=y1, z1=z1, x2=x2, y2=y2, z2=z2)

        for point in points:
            if point not in new_obstacles:
                self.env.map[point[2]][point[1]][point[0]] = 0

    def _bresenham_3d(self, x1, y1, z1, x2, y2, z2):
        points = []
        dx, dy, dz = abs(x2 - x1), abs(y2 - y1), abs(z2 - z1)
        xs, ys, zs = (1 if x2 > x1 else -1), (1 if y2 > y1 else -1), (1 if z2 > z1 else -1)

        if dx >= dy and dx >= dz:
            p1, p2 = 2 * dy - dx, 2 * dz - dx
            while x1 != x2:
                points.append((x1, y1, z1))
                x1 += xs
                if p1 >= 0:
                    y1 += ys
                    p1 -= 2 * dx
                if p2 >= 0:
                    z1 += zs
                    p2 -= 2 * dx
                p1 += 2 * dy
                p2 += 2 * dz
        elif dy >= dx and dy >= dz:
            p1, p2 = 2 * dx - dy, 2 * dz - dy
            while y1 != y2:
                points.append((x1, y1, z1))
                y1 += ys
                if p1 >= 0:
                    x1 += xs
                    p1 -= 2 * dy
                if p2 >= 0:
                    z1 += zs
                    p2 -= 2 * dy
                p1 += 2 * dx
                p2 += 2 * dz
        else:
            p1, p2 = 2 * dy - dz, 2 * dx - dz
            while z1 != z2:
                points.append((x1, y1, z1))
                z1 += zs
                if p1 >= 0:
                    y1 += ys
                    p1 -= 2 * dz
                if p2 >= 0:
                    x1 += xs
                    p2 -= 2 * dz
                p1 += 2 * dy
                p2 += 2 * dx

        points.append((x2, y2, z2))

        return points

if __name__ == "__main__":
    from src.compiler.converter.drone_api import DroneAPI
    import numpy as np
    np.set_printoptions(threshold=np.inf)

    drone = DroneAPI()
    drone.client.takeoffAsync().join()

    _, depth_img = drone.get_image()
    curr_pos = drone.current_position()
    camera_intrinsics = drone.get_camera_intrinsics()

    collision_manager = CollisionManager(camera_intrinsics=camera_intrinsics, max_x=10, max_y=10, max_z=3)

    import time
    start_time = time.time()
    collision_manager.update_state(depth_data=depth_img, curr_pos=curr_pos)
    print("--- %s seconds ---" % (time.time() - start_time))

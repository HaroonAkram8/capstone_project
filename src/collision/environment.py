import heapq
import random
import numpy as np
import pyvista as pv
import pyvistaqt as pvqt

class Environment():
    def __init__(self, max_x: int=100, max_y: int=100, max_z: int=10):
        self.x_offset = max_x
        self.y_offset = max_y
        self.max_z = max_z

        self.map = np.zeros(shape=(max_z, self.y_offset + max_y + 1, self.x_offset + max_x + 1))

        self.neighbors = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

        self.plotter = pvqt.BackgroundPlotter()

        self.ticker = 0
        array = self.map.transpose(2, 1, 0)
        self.obstacle_mesh = pv.ImageData(dimensions=np.array(array.shape) + 1)
    
    def set(self, val: int, x: int, y: int, z: int):
        self.map[-z + 1][y + self.y_offset][x + self.x_offset] = val
    
    def get(self, x: int, y: int, z: int):
        return self.map[-z + 1][y + self.y_offset][x + self.x_offset]
    
    def real_to_env(self, x: int, y: int, z: int):
        x = int(round(max(min(x + self.x_offset, self.x_offset * 2), -self.x_offset * 2)))
        y = int(round(max(min(y + self.y_offset, self.y_offset * 2), -self.y_offset * 2)))
        z = int(round(max(min(-z + 1, self.max_z - 1), 0)))

        return z, y, x
    
    def env_to_real(self, z: int, y: int, x: int):
        x -= self.x_offset
        y -= self.y_offset
        z = -z + 1

        return x, y, z
    
    def visualize(self, current_position: tuple, spacing: float=1.0, cube_size: float=1.0):
        self.plotter.view_isometric()
        self.plotter.clear()
        
        array = self.map.transpose(2, 1, 0)

        self.obstacle_mesh.overwrite(pv.ImageData(dimensions=np.array(array.shape) + 1))
        self.obstacle_mesh.cell_data["values"] = array.flatten(order="F")

        self.plotter.add_mesh(self.obstacle_mesh.threshold(0.5), color="red", show_edges=True, edge_color="black", name="mymesh")

        z, y, x = -current_position["z"] + 0.5, current_position["y"] + 0.5, current_position["x"] + 0.5

        z -= 1
        y += self.y_offset
        x += self.x_offset

        cube = pv.Cube(center=(x * spacing, y * spacing, z * spacing), x_length=cube_size, y_length=cube_size, z_length=cube_size)
        
        self.plotter.add_mesh(cube, color='green', show_edges=True, edge_color="black")

        self.plotter.render()
        self.plotter.app.processEvents()

        self.ticker += 1

    def get_path(self, start_pos: tuple, end_pos: tuple):
        goal = self.real_to_env(x=end_pos[0], y=end_pos[1], z=end_pos[2])
        if self.map[goal[0]][goal[1]][goal[2]] != 0:
            return None
        
        start = self.real_to_env(x=start_pos[0], y=start_pos[1], z=start_pos[2])

        path = self._a_star(start=start, goal=goal)
        path = self._simplify_path(path=path)

        return path
    
    def _is_collinear(self, p1, p2, p3):
        v1 = np.array(p2) - np.array(p1)
        v2 = np.array(p3) - np.array(p2)
        
        return np.all(np.cross(v1, v2) == 0)
    
    def _simplify_path(self, path):
        if len(path) < 3:
            return path
        
        simplified_path = [path[0]]
        
        for i in range(1, len(path) - 1):
            if not self._is_collinear(path[i-1], path[i], path[i+1]):
                simplified_path.append(path[i])
        
        simplified_path.append(path[-1])
        return simplified_path[1:]
    
    def _a_star(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, 0, start))

        came_from = {}
        g_score = {start: 0}
        f_score = {start: self._heuristic(start, goal)}

        while open_set:
            _, current_g, current = heapq.heappop(open_set)
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]
            
            for dz, dy, dx in self.neighbors:
                neighbor = (current[0] + dz, current[1] + dy, current[2] + dx)

                if not (0 <= neighbor[0] < self.map.shape[0] and 
                        0 <= neighbor[1] < self.map.shape[1] and 
                        0 <= neighbor[2] < self.map.shape[2]):
                    continue

                if self.map[neighbor] != 0:
                    continue

                tentative_g_score = current_g + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))

        return None
        
    def _heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
    
    def shape(self,):
        sh = self.map.shape
        return (sh[2], sh[1], sh[0])
        
    def _set_rand_obstacles(self,):
        x_max, y_max, z_max = self.shape()

        for x in range(x_max):
            for y in range(y_max):
                for z in range(z_max):
                    if random.random() < 0.1:
                        self.map[z][y][x] = 1

if __name__ == "__main__":
    import time
    env = Environment(max_x=10, max_y=10, max_z=5)

    # current_position = {
    #     "x": 2,
    #     "y": 10,
    #     "z": -3
    # }

    # while True:
    #     env._set_rand_obstacles()
    #     env.visualize(current_position=current_position)

    #     time.sleep(1)

    env._set_rand_obstacles()
    start = (9, 8, -3)
    goal = (-4, 5, -3)

    print(env.real_to_env(x=goal[0], y=goal[1], z=goal[2]))
    print(env.get_path(start, goal))

    print(env.env_to_real(x=6, y=15, z=4))
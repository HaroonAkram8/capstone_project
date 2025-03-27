import time
import pprint
import threading
from collections import deque

from src.compiler.converter.drone_api import DroneAPI
from src.compiler.converter.parser import ParameterParser
from src.compiler.converter.generate import ParameterGenerator
from src.globals import END, ROTATE, DEBUG_SEPARATOR, MOVE_POS, MOVE_DIST, MOVE_VEL
from src.vision.vision import VisionModel
from src.collision.collision_manager import CollisionManager

class Compiler():
    def __init__(self, drone_api: DroneAPI, param_gen: ParameterGenerator, debug: bool=False, simulation: bool=True, collision_avoidance: bool=True, display_collision_map: bool=False):
        self.drone_api = drone_api
        self.param_gen = param_gen
        self.debug = debug

        if debug:
            self.debug = debug
            self.debug_logs = deque()

            print(DEBUG_SEPARATOR)

        self.api_queue = deque()

        self.collision_avoidance = collision_avoidance
        if self.collision_avoidance:
            self.collision_manager = CollisionManager(simulation=simulation, camera_intrinsics=drone_api.get_camera_intrinsics(), max_x=100, max_y=100, max_z=20)
            self._startup_sequence()

            if display_collision_map:
                thread = threading.Thread(target=self.collision_manager.collision_visuals, args=self.drone_api.current_position, daemon=True)
                thread.start()

    def _startup_sequence(self,):
        for i in range(4):
            _, depth_img = self.drone_api.get_image()
            self.collision_manager.update_state(depth_data=depth_img, curr_pos=self.drone_api.current_position())
            self.drone_api.rotate_n_deg(yaw_rate=90, duration=1)

    def compile(self, instructions: str, run: bool=True, vision_model: VisionModel=None):
        parser = ParameterParser(instructions=instructions)
        parser.parse()
        commands, locate_objects = parser.cmd_seq()

        if len(locate_objects) == 0 or vision_model is None:
            self._compile_commands(commands=commands, run=run)
            return None

        num_rotations = 0
        all_found = False

        while not all_found and num_rotations < 4:
            rgb_img, depth_img = self.drone_api.get_image()

            if self.collision_avoidance:
                self.collision_manager.update_state(depth_data=depth_img, curr_pos=self.drone_api.current_position())

            vision_model.find_objects(rgb_image=rgb_img, depth_image=depth_img, classes=locate_objects)
            
            object_states = vision_model.get_object_states()
            all_found, obj_loc = self.get_object_locations(locate_objects=locate_objects, object_states=object_states)

            if not all_found:
                self.drone_api.rotate_n_deg(yaw_rate=90, duration=1)
                num_rotations += 1

        if num_rotations > 0:
            self.drone_api.rotate_n_deg(yaw_rate=-90 * num_rotations, duration=num_rotations)
        
        return obj_loc

    def get_object_locations(self, locate_objects, object_states):
        obj_loc = {}

        for obj in locate_objects:
            if obj not in object_states:
                return False, None
            
            obj_loc[obj] = object_states[obj].location
        
        return True, obj_loc

    def _compile_commands(self, commands: list, run: bool):
        for c, p in commands:
            self._add(cmd=c, params=p)

            if run:
                self.run()
        
        if self.collision_avoidance:
            _, depth_img = self.drone_api.get_image()
            self.collision_manager.update_state(depth_data=depth_img, curr_pos=self.drone_api.current_position())

    def run(self):
        while self.api_queue:
            func, args, is_async = self.api_queue.popleft()

            if self.debug:
                log = self.debug_logs.popleft()
                log["drone_state"] = self.drone_api.current_position()

                pprint.pprint(log)
                print(DEBUG_SEPARATOR)

            if is_async:
                func(**args).join()
                time.sleep(1)
                continue
            
            func(**args)
            time.sleep(1)

    def _add(self, cmd: str, params: dict):
        f = self.drone_api.get_function(cmd)

        if f is None:
            return
        
        f_params = self.param_gen.generate(cmd=cmd, parameters=params)
        is_async = cmd != END and cmd != ROTATE

        path = []
        if self.collision_avoidance and cmd in [MOVE_POS, MOVE_DIST, MOVE_VEL]:
            path = self._get_path(goal_position=f_params)

        if len(path) > 1:
            f = self.drone_api.get_function(MOVE_POS)
            
            for loc in path:
                temp_params = f_params.copy()
                temp_params['x'] = loc[0]
                temp_params['y'] = loc[1]
                temp_params['z'] = loc[2]

                self.api_queue.append((f, temp_params, True))
        else:
            self.api_queue.append((f, f_params, is_async))

        if self.debug:
            self._add_debug(cmd=cmd, params=params, f=f, f_params=f_params)
    
    def _get_path(self, goal_position: dict):
        curr_pos = self.drone_api.current_position()

        start_pos = (curr_pos['x'], curr_pos['y'], curr_pos['z'])
        end_pos = (goal_position['x'], goal_position['y'], goal_position['z'])

        path = self.collision_manager.get_path(start_pos=start_pos, end_pos=end_pos)
        return path

    def _add_debug(self, cmd, params, f, f_params):
        log = {
            "input": {
                "command": cmd,
                "parameters": params,
            },
            "output": {
                "API call": f,
                "API parameters": f_params,
            }
        }

        self.debug_logs.append(log)
    
    def _execute_all(self):
        while self.api_queue:
            self._execute()
    
    def _execute(self):
        if len(self.api_queue) == 0:
            return
        
        func, args, is_async = self.api_queue.popleft()

        if is_async:
            func(**args).join()
            return
        
        func(**args)

# Example usage
if __name__ == "__main__":
    example1 = "DISTANCE_MOVE forward_distance=5"

    drone = DroneAPI()
    vision_model = VisionModel()

    param_gen = ParameterGenerator(current_position=drone.current_position)
    compiler = Compiler(drone_api=drone, param_gen=param_gen, debug=False)
    compiler.compile(instructions=example1, vision_model=vision_model)
    # compiler.compile(instructions=example1, run=False)
    # compiler.run()

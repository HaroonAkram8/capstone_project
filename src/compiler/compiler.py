import pprint
from collections import deque

from src.compiler.converter.drone_api import DroneAPI
from src.compiler.converter.parser import ParameterParser
from src.compiler.converter.generate import ParameterGenerator
from src.globals import END, ROTATE, DEBUG_SEPARATOR
from src.vision.vision import VisionModel

class Compiler():
    def __init__(self, drone_api: DroneAPI, param_gen: ParameterGenerator, debug: bool=False):
        self.drone_api = drone_api
        self.param_gen = param_gen
        self.debug = debug

        if debug:
            self.debug = debug
            self.debug_logs = deque()

            print(DEBUG_SEPARATOR)

        self.api_queue = deque()
    
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
            vision_model.find_objects(rgb_image=rgb_img, depth_image=depth_img, classes=locate_objects)
            
            object_states = vision_model.get_object_states()
            all_found, obj_loc = self.get_object_locations(locate_objects=locate_objects, object_states=object_states)

            self.drone_api.rotate_n_deg(yaw_rate=90, duration=1)
            num_rotations += 1
        
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
                continue
            
            func(**args)

    def _add(self, cmd: str, params: dict):
        f = self.drone_api.get_function(cmd)

        if f is None:
            return
        
        f_params = self.param_gen.generate(cmd=cmd, parameters=params)
        is_async = cmd != END and cmd != ROTATE

        self.api_queue.append((f, f_params, is_async))

        if self.debug:
            self._add_debug(cmd=cmd, params=params, f=f, f_params=f_params)
    
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
    example1 = "TAKEOFF, ROTATE yaw=75 duration=3, DISTANCE_MOVE forward_distance=3, LAND"

    drone = DroneAPI()
    param_gen = ParameterGenerator(current_position=drone.current_position)
    compiler = Compiler(drone_api=drone, param_gen=param_gen, debug=True)

    compiler.compile(instructions=example1)

    # compiler.compile(instructions=example1, run=False)
    # compiler.run()

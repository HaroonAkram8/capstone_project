from collections import deque

from src.compiler.converter.drone_api import DroneAPI
from src.compiler.converter.parser import ParameterParser
from src.compiler.converter.generate import ParameterGenerator
from src.globals import CMD_KEY_WORDS

class Compiler():
    def __init__(self, drone_api: DroneAPI, param_gen: ParameterGenerator):
        self.drone_api = drone_api
        self.param_gen = param_gen
        self.api_queue = deque()
    
    def compile(self, instructions: str):
        parser = ParameterParser(instructions=instructions)
        parser.parse()
        commands = parser.cmd_seq()

        for c, p in commands:
            if c == CMD_KEY_WORDS["LOCATE"]:
                # TODO: vision model implementation
                continue

            self._add(cmd=c, params=p)

    def run(self):
        while self.api_queue:
            func, args, is_async = self.api_queue.popleft()

            if is_async:
                func(**args).join()
                continue
            
            func(**args)

    def _add(self, cmd: str, params: dict):
        f = self.drone_api.get_function(cmd)

        if f is None:
            return
        
        params = self.param_gen.generate(cmd=cmd, parameters=params)
        is_async = cmd != CMD_KEY_WORDS["END"]

        self.api_queue.append((f, params, is_async))
    
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
    example1 = "POSITION_MOVE x=3 y=5 z=2, DISTANCE_MOVE forward_distance=5, VELOCITY_MOVE forward_velocity=MODERATE duration=1, ROTATE yaw=-90, LAND"

    drone = DroneAPI()
    param_gen = ParameterGenerator(current_position=drone.current_position)
    compiler = Compiler(drone_api=drone, param_gen=param_gen)

    compiler.compile(instructions=example1.lower())
    compiler.run()

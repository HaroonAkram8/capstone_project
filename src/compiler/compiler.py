from collections import deque

from src.compiler.converter.drone_api import DroneAPI
from src.globals import (
    MOVE_POS, MOVE_VEL, ROTATE, TAKEOFF, LAND, END
)

class Compiler():
    def __init__(self, drone_api: DroneAPI):
        self.drone_api = drone_api
        self.api_queue = deque()

        # Create a dictionary mapping the command key to a parameter finding function
        # Use it in _get_params()
    
    def compile_and_run(self, drone_lang: str):
        # TODO: Apply drone language splitting etc.
        pass

        # TODO: For every individual drone language command, use _add
        pass

        # TODO: execute all drone api calls
        pass

    
    def _get_params(self, cmd: str):
        # TODO
        return {}
    
    def _add(self, cmd: str):
        f = self.drone_api.get_function(cmd)

        if f is None:
            return
        
        params = self._get_params(cmd=cmd)
        is_async = cmd != END

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
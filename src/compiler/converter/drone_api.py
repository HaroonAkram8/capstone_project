import airsim
import time

from src.globals import (
    MOVE_POS, MOVE_VEL, ROTATE, TAKEOFF, LAND, END
)

class DroneAPI():
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)

        self.functions = {
            MOVE_POS: self.client.moveToPositionAsync,
            MOVE_VEL: self.client.moveByVelocityAsync, # May need to be removed
            ROTATE: self.client.rotateToYawAsync,
            TAKEOFF: self.client.takeoffAsync,
            LAND: self.client.landAsync,
            END: self.__end__,
        }
    
    def __end__(self):
        self.client.armDisarm(False)
        self.client.enableApiControl(False)
    
    def get_function(self, key: str):
        if key not in self.functions:
            return None
        
        return self.functions[key]

# Example usage
if __name__ == "__main__":
    from collections import deque 

    drone = DroneAPI()
    
    command_order = [
        {"cmd": TAKEOFF, "params": {}},
        {"cmd": ROTATE, "params": {"yaw": 90}},
        {"cmd": MOVE_POS, "params": {"x": 1, "y": 2, "z": -5, "velocity": 1}},
        {"cmd": MOVE_POS, "params": {"x": 0, "y": 0, "z": -1, "velocity": 3}},
        {"cmd": LAND, "params": {}},
        {"cmd": END, "params": {}},
    ]

    queue = deque()

    for cmd_param in command_order:
        cmd = cmd_param["cmd"]
        params = cmd_param["params"]

        f = drone.get_function(cmd)

        if f is not None:
            queue.append((f, params, cmd != END))

    position = {"x": 5, "y": 10, "z": -7}
    rotate = {"angle_deg": 90, "rate_deg_per_sec": 30}

    while queue:
        func, args, is_async = queue.popleft()

        if is_async:
            func(**args).join()
            continue
        else:
            func(**args)
        
        time.sleep(1)
import airsim
import time
import math

from src.globals import (
    MOVE_POS, MOVE_DIST, MOVE_VEL, ROTATE, TAKEOFF, LAND, END, WAIT
)

class DroneAPI():
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)

        self.functions = {
            MOVE_POS: self.client.moveToPositionAsync,
            MOVE_DIST: self.client.moveToPositionAsync,
            MOVE_VEL: self.client.moveByVelocityAsync,
            ROTATE: self.client.rotateByYawRateAsync,
            TAKEOFF: self.client.takeoffAsync,
            LAND: self.client.landAsync,
            WAIT: self.__wait__,
            END: self.__end__,
        }
    
    def current_position(self, in_degrees: bool=False):
        state = self.client.getMultirotorState()

        position = state.kinematics_estimated.position
        orientation = state.kinematics_estimated.orientation

        position = {
            "x": position.x_val,
            "y": position.y_val,
            "z": position.z_val,
            "yaw": airsim.to_eularian_angles(orientation)[2]
        }

        if in_degrees:
            position["yaw"] = math.degrees(position["yaw"])

        return position
    
    def __wait__(self, duration):
        time.sleep(duration)
    
    def __end__(self):
        self.client.armDisarm(False)
        self.client.enableApiControl(False)
    
    def get_function(self, key: str):
        if key not in self.functions:
            return None
        
        return self.functions[key]

# Example usage
if __name__ == "__main__":
    drone = DroneAPI()
    print(drone.current_position())
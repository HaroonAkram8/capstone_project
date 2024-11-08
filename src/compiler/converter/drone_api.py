import airsim
import time
import math

from src.globals import (
    CMD_KEY_WORDS
)

class DroneAPI():
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)

        self.functions = {
            CMD_KEY_WORDS["MOVE_POS"]: self.client.moveToPositionAsync,
            CMD_KEY_WORDS["MOVE_DIST"]: self.client.moveToPositionAsync, #self.client.moveByVelocityAsync,
            CMD_KEY_WORDS["ROTATE"]: self.client.rotateToYawAsync,
            CMD_KEY_WORDS["TAKEOFF"]: self.client.takeoffAsync,
            CMD_KEY_WORDS["LAND"]: self.client.landAsync,
            CMD_KEY_WORDS["END"]: self.__end__,
        }
    
    def current_position(self):
        state = self.client.getMultirotorState()

        position = state.kinematics_estimated.position
        orientation = state.kinematics_estimated.orientation

        position = {
            "x": position.x_val,
            "y": position.y_val,
            "z": position.z_val,
            "yaw": airsim.to_eularian_angles(orientation)[2]
        }

        return position
    
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
import airsim
import time

from src.globals import (
    MOVE_POS, MOVE_VEL, ROTATE, TAKEOFF, LAND, END
)

class DroneController():
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

# Example usage
if __name__ == "__main__":
    drone = DroneController()

    position = {"x": 5, "y": 10, "z": -7}
    rotate = {"angle_deg": 90, "rate_deg_per_sec": 30}

    # Perform basic movements
    drone.functions[TAKEOFF]().join()
    # print(drone.client.getMultirotorState())
    drone.functions[ROTATE](rotate["angle_deg"]).join()
    print("movement 1 done")
    drone.functions[MOVE_POS](position["x"], position["y"], position["z"], velocity=5).join()
    print("movement 2 done")
    drone.functions[MOVE_POS](0, 0, -1, velocity=5).join()
    time.sleep(3)
    drone.functions[LAND]().join()

    drone.functions[END]()
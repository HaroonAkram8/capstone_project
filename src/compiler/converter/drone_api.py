import cv2
import time
import math
import airsim
import numpy as np

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
            ROTATE: self.rotate_n_deg, #self.client.rotateByYawRateAsync,
            TAKEOFF: self.client.takeoffAsync,
            LAND: self.client.landAsync,
            WAIT: self.__wait__,
            END: self.__end__,
        }
    
    
    def safe_land(self):
        # In future, ensure landing space is large enough to support drone
        self.client.landAsync().join()
        self.__end__()

    def get_image(self):
        responses = self.client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene, False, True),
            airsim.ImageRequest("0", airsim.ImageType.DepthPerspective, True)
        ])

        rgb_img, depth_img = None, None

        if responses:
            if responses[0].image_data_uint8:
                img_np = np.frombuffer(responses[0].image_data_uint8, dtype=np.uint8)
                rgb_img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

                # cv2.imshow("Drone Camera", rgb_img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

            if responses[1].image_data_float:
                depth_img = np.array(responses[1].image_data_float, dtype=np.float32)
        
        return rgb_img, depth_img
    
    def rotate_n_deg(self, yaw_rate, duration):
        self.client.rotateByYawRateAsync(yaw_rate, duration).join()
        self.client.rotateByYawRateAsync(0, 1).join()
    
    def current_position(self, in_degrees: bool=False):
        state = self.client.getMultirotorState()

        position = state.kinematics_estimated.position
        orientation = state.kinematics_estimated.orientation

        position = {
            "x": position.x_val,
            "y": position.y_val,
            "z": position.z_val,
            "yaw": airsim.to_eularian_angles(orientation)[2],
            "landed": state.landed_state == airsim.LandedState.Landed,
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
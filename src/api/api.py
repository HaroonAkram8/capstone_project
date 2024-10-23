import airsim
import time

class DroneController():
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)

        print("Drone initialized and ready.")
    
    def takeoff(self, altitude=5):
        print("Taking off...")

        self.client.takeoffAsync().join()
        self.client.moveToZAsync(-altitude, 5).join()

        print(f"Reached altitude: {altitude} meters")

    def land(self):
        print("Landing...")

        self.client.landAsync().join()
        self.client.armDisarm(False)
        self.client.enableApiControl(False)

        print("Drone landed and disarmed.")

# Example usage
if __name__ == "__main__":
    drone = DroneController()

    velocity = {"x": 5, "y": 10, "z": 7}
    rotate = {"angle_deg": 90, "rate_deg_per_sec": 30}

    # Perform basic movements
    drone.takeoff()
    drone.client.moveByVelocityAsync(velocity["x"], velocity["y"], velocity["z"], duration=5).join()
    print("movement 1 done")
    drone.client.moveByVelocityAsync(-velocity["x"], -velocity["y"], -velocity["z"], duration=5).join()
    print("movement 2 done")
    drone.client.goHomeAsync().join()
    print("Returned home")
    drone.land()

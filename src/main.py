from src.drone_manager import DroneManager

def main():
    drone = DroneManager(model_name="phi3_mini")
    drone.listen()

if __name__ == "__main__":
    main()
from src.drone_manager import DroneManager

def main():
    drone = DroneManager()
    drone.listen()

if __name__ == "__main__":
    main()
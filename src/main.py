from src.drone_manager import DroneManager

def main():
    drone = DroneManager()
    drone.listen(model="llama3", stream=True)

if __name__ == "__main__":
    main()
from src.drone_manager import DroneManager
from src.llm.llm import Models

def main():
    drone = DroneManager(model=Models.PHI3_MINI)
    drone.listen()

if __name__ == "__main__":
    main()
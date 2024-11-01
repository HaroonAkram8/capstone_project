from src.drone_manager import DroneManager
from src.llm.llm import Models

def main():
    drone = DroneManager(model=Models.LLAMA3)
    drone.listen()

def run_phi3_mini():
    "Runs the phi3_mini model with our system prompt"
    main(Models.PHI3_MINI)

if __name__ == "__main__":
    run_phi3_mini()

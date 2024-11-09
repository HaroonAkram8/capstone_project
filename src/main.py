from src.drone_manager import DroneManager
from src.llm.llm import Models

def main():
    with open("./system_prompts/llama3_1.txt", "r") as file:
        system_prompt = file.read()

    drone = DroneManager(model=Models.LLAMA3, system_prompt=system_prompt)
    drone.listen()

if __name__ == "__main__":
    main()
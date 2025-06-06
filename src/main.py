from src.drone_manager import DroneManager
from src.llm.llm import Models

def main():
    with open("./system_prompts/llama3_1.txt", "r") as file:
        system_prompt = file.read()

    drone = DroneManager(llm_model=Models.LLAMA3_1, system_prompt=system_prompt, enable_speech=False, collision_avoidance=False)
    drone.listen()

if __name__ == "__main__":
    main()

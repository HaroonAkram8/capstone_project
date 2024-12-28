from src.drone_manager import DroneManager
from src.llm.llm import Models

def main(model: Models):
    "Takes a model and runs it with our system prompt"
    system_prompt = ""
    with open("./system_prompts/default_system_prompt.txt", "r") as file:
        system_prompt = file.read().lower()

    drone = DroneManager(model=model, system_prompt=system_prompt)
    drone.listen()

def run_llama3_1():
    "Runs the llama3_1 model with our system prompt"
    main(Models.LLAMA3_1)

def run_phi3_mini():
    "Runs the phi3_mini model with our system prompt"
    main(Models.PHI3_MINI)

if __name__ == "__main__":
    run_phi3_mini()

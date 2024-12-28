from src.drone_manager_factory import DroneManagerFactory, DroneManagerTypes
from src.llm.llm import Models


def main(model: Models, drone_manager_type: DroneManagerTypes):
    "Takes a model and runs it with our system prompt"
    system_prompt = ""
    with open("./system_prompts/default_system_prompt.txt", "r") as file:
        system_prompt = file.read().lower()

    drone_factory = DroneManagerFactory()
    drone = drone_factory.create(
        drone_type=drone_manager_type, model=model, system_prompt=system_prompt
    )
    drone.listen()


def run_llama3_1(drone_manager_type: DroneManagerTypes):
    "Runs the llama3_1 model with our system prompt"
    main(Models.LLAMA3_1, drone_manager_type)


def run_phi3_mini(drone_manager_type: DroneManagerTypes):
    "Runs the phi3_mini model with our system prompt"
    main(Models.PHI3_MINI, drone_manager_type)


if __name__ == "__main__":
    drone_manager_type = DroneManagerTypes.ConcreteDrone
    run_llama3_1(drone_manager_type)

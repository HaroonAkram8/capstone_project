import abc

from src.llm.llm import LLM, Models
from src.speech_to_text.speech_to_text import speech_to_text
from src.compiler.converter.drone_api import DroneAPI
from src.compiler.converter.generate import ParameterGenerator
from src.compiler.compiler import Compiler

class IDroneManager(abc.ABC):
    def __init__(self, model: Models, system_prompt: str) -> None:
        ...

    def listen(self) -> None:
        ...

class TestDroneManager(IDroneManager):
    def __init__(self, model: Models, system_prompt: str) -> None:
        print(system_prompt)
        self.model = LLM(model=model, system_prompt=system_prompt)

    def listen(self) -> None:
        while(True):
            query = speech_to_text()

            if query is None:
                continue
            if "stop listening" in query:
                break

            prompt = query
            response = self.model.chat(prompt=prompt)

            print(response)
            print()


class DroneManager(IDroneManager):
    def __init__(self, model: Models, system_prompt: str) -> None:
        self.model = LLM(model=model, system_prompt=system_prompt)

        self.drone = DroneAPI()
        self.generator = ParameterGenerator(current_position=self.drone.current_position)

        self.compiler = Compiler(drone_api=self.drone, param_gen=self.generator)
    
    def listen(self) -> None:
        while(True):
            query = speech_to_text()

            if query is None:
                continue
            if "stop listening" in query:
                break

            position = {"x": 5.0, "y": 7.0, "z": 3.0, "yaw": 34.0}
            prompt = f"Drone State: {str(position)}\nMovement Instructions: {query}"
            prompt = query
            response = self.model.chat(prompt=prompt)

            print(response)
            print()

            self.compiler.compile(instructions=response)
            self.compiler.run()

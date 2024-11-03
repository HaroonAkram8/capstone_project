from src.llm.llm import LLM, Models
from src.speech_to_text.speech_to_text import speech_to_text
from src.compiler.converter.drone_api import DroneAPI
from src.compiler.converter.generate import ParameterGenerator
from src.compiler.compiler import Compiler

class DroneManager:
    def __init__(self, model: Models) -> None:
        self.model = LLM(model=model)

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

            prompt = f"Drone State: {str(self.drone.current_position())}\nMovement Instructions: {query}"
            response = self.model.chat(prompt=prompt)

            print(response)
            print()

            self.compiler.compile(instructions=response)
            self.compiler.run()

from src.llm.llm import LLM, Models
from src.speech_to_text.speech_to_text import speech_to_text
from src.compiler.converter.drone_api import DroneAPI
from src.compiler.converter.generate import ParameterGenerator
from src.compiler.compiler import Compiler

class DroneManager:
    def __init__(self, model: Models) -> None:
        self.model = LLM(model=model)

        drone = DroneAPI()
        generator = ParameterGenerator(current_position=drone.current_position)

        self.compiler = Compiler(drone_api=drone, param_gen=generator)
    
    def listen(self) -> None:
        while(True):
            query = speech_to_text()
            
            if query is None:
                continue
            if "stop listening" in query:
                break

            response = self.model.chat(prompt=query)

            print(response)
            print()

            self.compiler.compile(instructions=response)
            self.compiler.run()

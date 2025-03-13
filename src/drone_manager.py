from src.llm.llm import LLM, Models

from src.speech_to_text.speech_to_text import speech_to_text

from src.compiler.converter.drone_api import DroneAPI
from src.compiler.converter.generate import ParameterGenerator
from src.compiler.compiler import Compiler

from src.vision.vision import VisionModel

class DroneManager:
    def __init__(self, llm_model: Models, system_prompt: str) -> None:
        self.llm_model = LLM(model=llm_model, system_prompt=system_prompt)
        self.llm_model.chat(prompt="Hello world")

        input("Large Language Model loaded, press Enter to set up Vision Model...")

        self.vision_model = VisionModel()

        input("Vision Model loaded, press Enter to set up API...")

        self.drone = DroneAPI()
        self.generator = ParameterGenerator(current_position=self.drone.current_position)

        self.compiler = Compiler(drone_api=self.drone, param_gen=self.generator)

        input("API loaded, press Enter to start...")
    
    def listen(self) -> None:
        while(True):
            input("Press Enter to continue...")
            query = speech_to_text()
            
            if query is None:
                continue
            if "stop listening" in query:
                break

            prompt = f"Drone State: {str(self.drone.current_position(in_degrees=True))}\nMovement Instructions: {query}"
            obj_loc = self._compile_and_run(prompt=prompt)

            if obj_loc is None:
                continue

            prompt = f"Drone State: {str(self.drone.current_position(in_degrees=True))}\nObject Locations: {str(obj_loc)}\nMovement Instructions: {query}"
            self._compile_and_run(prompt=prompt)
    
    def _compile_and_run(self, prompt: str):
        print(prompt)
        
        response = self.llm_model.chat(prompt=prompt)
        print(response)

        obj_loc = self.compiler.compile(instructions=response, vision_model=self.vision_model)
        return obj_loc
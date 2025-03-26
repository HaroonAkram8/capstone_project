import signal
import sys

from src.llm.llm import LLM, Models

from src.speech_to_text.speech_to_text import speech_to_text

from src.compiler.converter.drone_api import DroneAPI
from src.compiler.converter.generate import ParameterGenerator
from src.compiler.compiler import Compiler

from src.vision.vision import VisionModel

from src.globals import TAKEOFF, STOP, LOCATE

class DroneManager:
    def __init__(self, llm_model: Models, system_prompt: str, enable_speech: bool=True, simulation: bool=True) -> None:
        self.enable_speech = enable_speech

        print("Loading the Large Language Model...")

        self.llm_model = LLM(model=llm_model, system_prompt=system_prompt)
        self.llm_model.chat(prompt="Hello world")

        input("Large Language Model loaded, press Enter to set up Vision Model...")

        self.vision_model = VisionModel(simulation=simulation)

        input("Vision Model loaded, press Enter to set up API...")

        self.drone = DroneAPI()
        
        def cleanup(signum, frame):
            print(f"Received signal {signum}. Cleaning up and landing...")
            self.drone.safe_land()
            
            sys.exit(0)

        signal.signal(signal.SIGINT, cleanup)
        signal.signal(signal.SIGTERM, cleanup)

        self.vision_model.set_current_location(current_position=self.drone.current_position)
        self.vision_model.set_camera_intrinsics(camera_intrinsics=self.drone.get_camera_intrinsics())

        self.generator = ParameterGenerator(current_position=self.drone.current_position)
        self.compiler = Compiler(drone_api=self.drone, param_gen=self.generator)

        input("API loaded, press Enter to start...")
    
    def listen(self) -> None:
        while(True):
            print("-" * 75)

            query = ""
            if self.enable_speech:
                query = speech_to_text()
            else:
                query = input("Awaiting written instructions...\n")
                print()
            
            if query is None:
                continue
            if STOP in query:
                self.drone.safe_land()
                break
            
            curr_pos = self.drone.current_position(in_degrees=True, round_to_n=2)
            prompt = f"Drone State: {str(curr_pos)}\nMovement Instructions: {query}"
            obj_loc = self._compile_and_run(prompt=prompt)

            if obj_loc is not None:
                print()
                prompt = f"Drone State: {str(curr_pos)}\nObject Locations: {str(obj_loc)}\nMovement Instructions: {query}"
                self._compile_and_run(prompt=prompt, locate=False)

            input("Press Enter to continue...")
    
    def _compile_and_run(self, prompt: str, locate: bool=True):
        print(prompt)
        
        response = self.llm_model.chat(prompt=prompt)
        response = self._land_state_handler(response=response)
        print(response)

        if not locate and LOCATE in response:
            return None

        obj_loc = self.compiler.compile(instructions=response, vision_model=self.vision_model)
        return obj_loc
    
    def _land_state_handler(self, response: str):
        drone_state = self.drone.current_position()

        if drone_state["landed"] and not response.startswith(TAKEOFF):
            response = TAKEOFF + ", " + response

        return response
from src.llm.llm import LLM
from src.speech_to_text.speech_to_text import speech_to_text

class DroneManager:
    def __init__(self, model_name: str) -> None:
        self.model = LLM(model_name=model_name)
    
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

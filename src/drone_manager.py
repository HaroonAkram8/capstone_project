from src.llm.llm import LLM, Models
from src.speech_to_text.speech_to_text import speech_to_text

class DroneManager:
    def __init__(self, model: Models, system_prompt: str) -> None:
        self.model = LLM(model=model, system_prompt=system_prompt)
    
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

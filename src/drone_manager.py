from src.llm.llama import Llama
from src.speech_to_text.speech_to_text import speech_to_text

class DroneManager:
    def __init__(self) -> None:
        self.llama = Llama()
    
    def listen(self, model: str, stream: bool=True) -> None:
        while(True):
            query = speech_to_text()
            
            if query is None:
                continue
            if "stop listening" in query:
                break

            response = self.llama.chat(model=model, prompt=query, stream=stream)

            if stream:
                for chunk in response:
                    print(chunk['message']['content'], end='', flush=True)
                print()
            else:
                print(response['message']['content'])
            print()
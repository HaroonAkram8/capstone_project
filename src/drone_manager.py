from src.speech_to_text.speech_to_text import speech_to_text

class DroneManager:
    def __init__(self) -> None:
        pass
    
    def listen(self) -> None:
        while(True):
            query = speech_to_text()
            
            if query is not None and "stop listening" in query:
                break
import ollama
from enum import Enum

from src.globals import DEFAULT_SYSTEM_PROMPT

class Models(Enum):
    LLAMA3_1 = "llama3.1"
    LLAMA3_1_70 = "llama3.1:70b"
    LLAMA3 = "llama3"
    PHI3_MINI = "phi3:mini"

class LLM:
    def __init__(self, model: Models):
        self.model_name = model.value
    
    def chat(self, prompt: str):
        response = ollama.chat(
            model=self.model_name,
            messages=[DEFAULT_SYSTEM_PROMPT[self.model_name], {'role': 'user', 'content': prompt}],
            stream=False,
        )

        return response['message']['content']

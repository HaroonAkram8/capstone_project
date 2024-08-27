import ollama
from enum import Enum

from src.globals import DEFAULT_SYSTEM_PROMPT

class Models(Enum):
    PHI3_MINI = "phi3:mini"
    LLAMA3 = "llama3"

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
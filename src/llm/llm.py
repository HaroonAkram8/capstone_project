import ollama
from enum import Enum


class Models(Enum):
    LLAMA3_1 = "llama3.1"
    LLAMA3 = "llama3"
    PHI3_MINI = "phi3:mini"

class LLM:
    def __init__(self, model: Models, system_prompt: str):
        self.model_name = model.value
        self.system_prompt = {"role": "system", "content": system_prompt}
    
    def chat(self, prompt: str):
        response = ollama.chat(
            model=self.model_name,
            messages=[self.system_prompt, {'role': 'user', 'content': prompt}],
            stream=False,
        )

        return response['message']['content'].strip('"')

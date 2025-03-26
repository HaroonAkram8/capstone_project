import ollama
from enum import Enum

class Models(Enum):
    LLAMA3_3 = "llama3.3"
    LLAMA3_2 = "llama3.2"
    LLAMA3_1 = "llama3.1"
    LLAMA3_1_70 = "llama3.1:70b"
    LLAMA3 = "llama3"
    PHI3_MINI = "phi3:mini"
    DEEPSEEK = "deepseek-r1"
    LLAMA_TUNED = "tzprogrammer/llama-drone"

class LLM:
    def __init__(self, model: Models, system_prompt: str):
        self.model_name = model.value
        self.system_prompt = {"role": "system", "content": system_prompt}

    def chat(self, prompt: str, temperature: float = 0.2):
        response = ollama.chat(
            model=self.model_name,
            messages=[self.system_prompt, {"role": "user", "content": prompt}],
            options={"temperature": temperature},
            stream=False,
        )

        return response["message"]["content"].strip('"')

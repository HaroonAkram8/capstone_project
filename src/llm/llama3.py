import ollama
from src.globals import LLAMA3_DEFAULT_SYSTEM_PROMPT

class Llama3:
    def chat(self, prompt: str):
        response = ollama.chat(
            model="llama3",
            messages=[LLAMA3_DEFAULT_SYSTEM_PROMPT, {'role': 'user', 'content': prompt}],
            stream=False,
        )

        return response['message']['content']
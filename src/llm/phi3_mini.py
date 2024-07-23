import ollama

from src.globals import PHI3_MINI_DEFAULT_SYSTEM_PROMPT

class Phi3_Mini:
    def chat(self, prompt: str):
        response = ollama.chat(
            model="phi3:mini",
            messages=[PHI3_MINI_DEFAULT_SYSTEM_PROMPT, {'role': 'user', 'content': prompt}],
            stream=False,
        )

        return response['message']['content']

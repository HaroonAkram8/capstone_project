import ollama

class Llama:
    def chat(self, model: str, prompt: str, stream: bool=True):
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            stream=stream,
        )

        return response
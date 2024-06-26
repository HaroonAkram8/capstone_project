import ollama

class Llama3:
    def chat(self, prompt: str):
        response = ollama.chat(
            model="llama3",
            messages=[{'role': 'user', 'content': prompt}],
            stream=False,
        )

        return response['message']['content']
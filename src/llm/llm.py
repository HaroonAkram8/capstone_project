import ollama

from src.globals import DEFAULT_SYSTEM_PROMPT

class LLM:
    def __init__(self, model_name: str):
        # Import statements are done in these if blocks so that we don't overwrite the setting of environment variables
        if model_name not in ["phi3:mini", "llama3"]:
            raise ValueError("Parameter 'model_name' must be 'phi3:mini' or 'llama3'")
        
        self.model_name = model_name
    
    def chat(self, prompt: str):
        response = ollama.chat(
            model=self.model_name,
            messages=[DEFAULT_SYSTEM_PROMPT[self.model_name], {'role': 'user', 'content': prompt}],
            stream=False,
        )

        return response['message']['content']
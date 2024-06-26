class LLM:
    def __init__(self, model_name: str):
        # Import statements are done in these if blocks so that we don't overwrite the setting of environment variables
        if model_name == "phi3_mini":
            from src.llm.phi3_mini import Phi3_Mini
            self.model = Phi3_Mini()

        elif model_name == "llama3":
            from src.llm.llama3 import Llama3
            self.model = Llama3()

        else:
            raise ValueError("Parameter must be 'phi3_mini' or 'llama3'")
    
    def chat(self, prompt: str):
        return self.model.chat(prompt=prompt)
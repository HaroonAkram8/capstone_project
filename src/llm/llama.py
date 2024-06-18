import ollama

class Llama:
    def chat(self, model: str, prompt: str, stream: bool=True):
        '''
        stream: Setting to true will give you the response as it generates (an iterator), setting to false will only return a response after it is done generating the text (a str).
        '''

        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            stream=stream,
        )

        return response
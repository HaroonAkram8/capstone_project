from enum import Enum
from abc import ABC

import ollama

from src.globals import DEFAULT_SYSTEM_PROMPT


class Models(Enum):
    LLAMA3_1 = "llama3.1"
    LLAMA3 = "llama3"
    PHI3_MINI = "phi3:mini"

class ILLM(ABC):
    def chat(self, prompt: str) -> str: ...


class Decorator(ILLM, ABC):
    def __init__(self, llm: ILLM):
        self.llm = llm

    def chat(self, prompt: str) -> str: ...


class Thinker(Decorator):
    def __init__(self, drone_llm: ILLM, regular_llm: ILLM):
        Decorator.__init__(self, drone_llm)
        self.regular_llm = regular_llm

    def chat(self, prompt: str) -> str:
        thought_process = self.regular_llm.chat(prompt)
        refined_prompt = prompt + "\n" + thought_process
        return self.llm.chat(refined_prompt)


class TranslateLLM(ILLM):
    def __init__(self, model: Models):
        self.model_name = model.value

        system_prompt_content = ""
        system_prompt_path = "./system_prompts/translate_system_prompt.txt"
        with open(system_prompt_path, "r") as file:
            system_prompt_content = file.read().lower()

        self.system_prompt = {"role": "system", "content": system_prompt_content}

    def chat(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model_name,
            messages=[self.system_prompt, {"role": "user", "content": prompt}],
            stream=False,
        )

        return response["message"]["content"].strip('"')


class RegularLLM(ILLM):
    def __init__(self, model: Models):
        self.model_name = model.value

        system_prompt_content = ""
        system_prompt_path = "./system_prompts/regular_system_prompt.txt"
        with open(system_prompt_path, "r") as file:
            system_prompt_content = file.read().lower()

        self.system_prompt = {"role": "system", "content": system_prompt_content}

    def chat(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model_name,
            messages=[self.system_prompt, {"role": "user", "content": prompt}],
            stream=False,
        )

        return response["message"]["content"].strip('"')

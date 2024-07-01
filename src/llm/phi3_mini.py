import os
import torch

from src.globals import PHI_3_MINI_PATH, PHI_3_MINI_CHECKPOINT

# HuggingFace cache directory must be set before importing from transformers library
os.environ['HF_HOME'] = PHI_3_MINI_PATH
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

DEFAULT_GEN_ARGS = {
    "max_new_tokens": 500,
    "return_full_text": False,
    "do_sample": False,
}

class Phi3_Mini:
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(PHI_3_MINI_CHECKPOINT, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(PHI_3_MINI_CHECKPOINT, trust_remote_code=True, torch_dtype="auto", device_map=device)

        self.pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    def chat(self, prompt: str, generation_args: dict=DEFAULT_GEN_ARGS):
        input = {"role": "user", "content": prompt},
        output = self.pipe(input, **generation_args)

        return output[0]['generated_text']

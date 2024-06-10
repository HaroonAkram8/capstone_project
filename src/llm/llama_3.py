# # import transformers
# # import torch

# # model_id = "meta-llama/Meta-Llama-3-8B"
# # # model_id = "./models/models--meta-llama--Meta-Llama-3-8B/snapshots/62bd457b6fe961a42a631306577e622c83876cb6"

# # pipeline = transformers.pipeline(
# #     "text-generation",
# #     model=model_id,
# #     model_kwargs={
# #         "torch_dtype": torch.float16,
# #         "quantization_config": {"load_in_4bit": True},
# #         "low_cpu_mem_usage": True
# #     },
# #     device_map="auto",
# #     cache_dir='./models',
# #     token='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'
# # )
# # pipeline("Hey how are you doing today?")

# from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TextStreamer
# import torch

# # model_id = "meta-llama/Meta-Llama-3-8B"
# model_id = "./models/models--meta-llama--Meta-Llama-3-8B/snapshots/62bd457b6fe961a42a631306577e622c83876cb6/"

# quantization_config = BitsAndBytesConfig(
#     load_in_4bit=True
# )

# # tokenizer = AutoTokenizer.from_pretrained(model_id, token='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', cache_dir='./models', trust_remote_code=True)
# # model = AutoModelForCausalLM.from_pretrained(model_id, token='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', cache_dir='./models', quantization_config=quantization_config, trust_remote_code=True).eval()

# tokenizer = AutoTokenizer.from_pretrained(model_id, local_files_only=True, trust_remote_code=True)
# model = AutoModelForCausalLM.from_pretrained(model_id, local_files_only=True, quantization_config=quantization_config, trust_remote_code=True).eval()

# system= """\n\n You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. If you don't know the answer to a question, please don't share false information."""
# user= "\n\n You are an expert in astronomy. Can you tell me 5 fun facts about the universe?"
# model_answer_1 = 'None'

# llama_prompt_tempate = f"""
# <|begin_of_text|>\n<|start_header_id|>system<|end_header_id|>{system}
# <|eot_id|>\n<|start_header_id|>user<|end_header_id|>{user}
# <|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>{model_answer_1}<|eot_id|>
# """

# inputs = tokenizer(llama_prompt_tempate, return_tensors="pt").input_ids

# streamer = TextStreamer(tokenizer, skip_prompt=True)

# with torch.no_grad():
#     output_ids = model.generate(
#         inputs,
#         streamer=streamer,
#         pad_token_id=128001,
#         eos_token_id=128001,
#         max_new_tokens=300,
#         repetition_penalty=1.5
#     )

# # Decode the generated text
# output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

# print(output_text)
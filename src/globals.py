# Model Paths
PHI_3_MINI_PATH = "./models/base_phi_3_mini"
LLAMA_3_PATH = "./models/base_llama_3"

# HuggingFace Model Checkpoints
PHI_3_MINI_CHECKPOINT = "microsoft/Phi-3-mini-4k-instruct"
LLAMA_3_CHECKPOINT = "meta-llama/Meta-Llama-3-8B"

# System Prompts
LLAMA3_DEFAULT_SYSTEM_PROMPT = {"role": "system", "content": "You convert sentences into instructions for a drone. These are the possible drone instructions: UP, DOWN, LEFT, RIGHT, FORWARD, BACKWARD, ROTATE X (where X is the direction). Each instruction must be separated by a comma."}
PHI3_MINI_DEFAULT_SYSTEM_PROMPT = {"role": "system", "content": "You convert sentences into instructions for a drone. These are the possible drone instructions: UP, DOWN, LEFT, RIGHT, FORWARD, BACKWARD, ROTATE X (where X is the direction). Each instruction must be separated by a comma."}

# Model Paths
LLAMA_3_1_PATH = "./models/base_llama_3.1"
LLAMA_3_PATH = "./models/base_llama_3"
PHI_3_MINI_PATH = "./models/base_phi_3_mini"

# HuggingFace Model Checkpoints
LLAMA_3_1_BASE_CHECKPOINT = "meta-llama/Meta-Llama-3.1-8B"
LLAMA_3_BASE_CHECKPOINT = "meta-llama/Meta-Llama-3-8B"
PHI_3_MINI_CHECKPOINT = "microsoft/Phi-3-mini-4k-instruct"

# System Prompts
DEFAULT_SYSTEM_PROMPT = {
    "llama3.1": {"role": "system", "content": "You convert sentences into instructions for a drone. These are the possible drone instructions: UP, DOWN, LEFT, RIGHT, FORWARD, BACKWARD, ROTATE X (where X is the direction). Each instruction must be separated by a comma."},
    "llama3": {"role": "system", "content": "You convert sentences into instructions for a drone. These are the possible drone instructions: UP, DOWN, LEFT, RIGHT, FORWARD, BACKWARD, ROTATE X (where X is the direction). Each instruction must be separated by a comma."},
    "phi3:mini": {"role": "system", "content": "You convert sentences into instructions for a drone. These are the possible drone instructions: UP, DOWN, LEFT, RIGHT, FORWARD, BACKWARD, ROTATE X (where X is the direction). Each instruction must be separated by a comma."}
}

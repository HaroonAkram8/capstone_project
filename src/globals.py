# Model Paths
LLAMA_3_1_PATH = "./models/base_llama_3.1"
LLAMA_3_PATH = "./models/base_llama_3"
PHI_3_MINI_PATH = "./models/base_phi_3_mini"
PHI_3_MINI_INSTRUCT_PATH = "./models/instruct_phi_3_mini"

# HuggingFace Model Checkpoints
LLAMA_3_1_BASE_CHECKPOINT = "meta-llama/Meta-Llama-3.1-8B"
LLAMA_3_1_INSTRUCT_CHECKPOINT = "meta-llama/Meta-Llama-3.1-8B-Instruct"
LLAMA_3_BASE_CHECKPOINT = "meta-llama/Meta-Llama-3-8B"
LLAMA_3_INSTRUCT_CHECKPOINT = "meta-llama/Meta-Llama-3-8B-Instruct"
PHI_3_MINI_CHECKPOINT = "microsoft/Phi-3-mini-4k-instruct"

# System Prompts
DEFAULT_SYSTEM_PROMPT = {
    "llama3.1": {"role": "system", "content": "You convert sentences into instructions for a drone. These are the possible drone instructions: UP, DOWN, LEFT, RIGHT, FORWARD, BACKWARD, ROTATE X (where X is the direction). Each instruction must be separated by a comma."},
    "llama3": {"role": "system", "content": "You convert sentences into instructions for a drone. These are the possible drone instructions: UP, DOWN, LEFT, RIGHT, FORWARD, BACKWARD, ROTATE X (where X is the direction). Each instruction must be separated by a comma."},
    "phi3:mini": {"role": "system", "content": "You convert sentences into instructions for a drone. These are the possible drone instructions: UP, DOWN, LEFT, RIGHT, FORWARD, BACKWARD, ROTATE X (where X is the direction). Each instruction must be separated by a comma."}
}

# Airsim Mapping Keys
CMD_KEY_WORDS = {
    "MOVE_POS": "move",
    "MOVE_REL": "relative_move",
    "ROTATE": "rotate",
    "TAKEOFF": "takeoff",
    "LAND": "land",
    "LOCATE": "locate",
    "END": "end",
}

# Instruction Splits
INSTRUCTION_MARKER = ", "
PARAMETER_MARKER = " "
ASSIGNMENT_MARKER = "="

# Default Drone Language Key Words
KEY_WORDS = {
    "SLOW": 1,
    "MODERATE": 3,
    "FAST": 5,
    "SHORT": 1,
    "INTERMEDIATE": 3,
    "FAR": 5
}
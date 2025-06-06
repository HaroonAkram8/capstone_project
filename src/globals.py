# Stop Drone Manager Instruction
STOP = "stop drone"

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

# Instruction Splits
INSTRUCTION_MARKER = ", "
PARAMETER_MARKER = " "
ASSIGNMENT_MARKER = "="

# Airsim Mapping Keys
MOVE_POS = "position_move"
MOVE_DIST = "distance_move"
MOVE_VEL = "velocity_move"
ROTATE = "rotate"
WAIT = "wait"
TAKEOFF = "takeoff"
LAND = "land"
LOCATE = "locate"
END = "end"

CMD_KEY_WORDS = {
    MOVE_POS: MOVE_POS,
    MOVE_DIST: MOVE_DIST,
    MOVE_VEL: MOVE_VEL,
    ROTATE: ROTATE,
    WAIT: WAIT,
    TAKEOFF: TAKEOFF,
    LAND: LAND,
    LOCATE: LOCATE,
    END: END,
}

# Default Drone Language Key Words
KEY_WORDS = {
    "slow": 1, # velocity
    "moderate": 3, # velocity
    "fast": 5, # velocity
    "short": 1, # distance
    "medium": 3, # distance
    "far": 5, # distance
    "quick": 1, # time
    "intermediate": 3, # time
    "long": 5, # time
}

# Separators
DEBUG_SEPARATOR = "=" * 175
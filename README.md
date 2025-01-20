# capstone_project

## Getting Started

To find our starting guide for our team's practises, go to the link [HERE](https://docs.google.com/document/d/1EiJclbaxjeyAQCGsPbYKBOZUCOdSMVnfGlibOup19aQ/edit).

### Environment Setup

Run the following commands to setup your virtual environment:

```
python3.11 -m venv ./capstone_venv   # create virtual environment for installing dependencies in root directory
./capstone_venv/Scripts/activate  # run this to activate your virtual environment if it isn't activated already
```

To install packages into your environment, run:

```
pip install -r requirements.txt
```

To add/remove dependencies, manually add/remove them from requirements.txt

### Ollama Setup

You need to have a local ollama server running to be able to continue. To do this:

- Download: https://ollama.com/
- Run a Llama3.2: `ollama run llama3.2`
- Run a Llama3.1: `ollama run llama3.1`
- Run a Llama3.1 70B: `ollama run llama3.1:70b`
- Run a Llama3: `ollama run llama3`
- Run a Phi3 Mini: `ollama run phi3:mini`

### PyTorch Setup

Install torch with CUDA from https://pytorch.org/get-started/locally/. This project uses torch 2.2.0 with CUDA 12.1 so use other versions at your own risk. If you do not have a cuda enabled machine, download regular torch 2.2.0.

## Drone Manager

The DroneManager class is responsible for controlling the drone based on user input and its environment. This is where all parts of our project come together to communicate with the drone.

The following describes the available functions in the DroneManager class:

**listen(self, model: str, stream: bool=True):** Continuously listen to a microphone and register user input. If a user says **"stop listening"** at any point in a sentence, end listening operations.
- model (str): The model which you would like to use with Ollama. Must be one of the following => ['phi3_mini', 'llama3']

```
from src.drone_manager import DroneManager

drone = DroneManager(model_name="phi3_mini")
drone.listen()
```

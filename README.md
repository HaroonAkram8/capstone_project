# capstone_project

## Getting Started

To find our starting guide for our team's practises, go to the link [HERE](https://docs.google.com/document/d/1EiJclbaxjeyAQCGsPbYKBOZUCOdSMVnfGlibOup19aQ/edit).

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

## Drone Manager

The DroneManager class is responsible for controlling the drone based on user input and its environment. This is where all parts of our project come together to communicate with the drone.

The following describes the available functions in the DroneManager class:

**listen(self):** Continuously listen to a microphone and register user input. If a user says **"stop listening"** at any point in a sentence, end listening operations.

```
from src.drone_manager import DroneManager

drone = DroneManager()
drone.listen()
```
# capstone_project

## Getting Started

To find our starting guide for our team's practises, go to the link [HERE](https://docs.google.com/document/d/1EiJclbaxjeyAQCGsPbYKBOZUCOdSMVnfGlibOup19aQ/edit).

We use python3.11 for development so make sure you have it downloaded.

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

To add/remove dependencies, use:

```
pip install/uninstall [package_name]
pip freeze > requirements.txt
```

### Ollama Setup

You need to have a local ollama server running to be able to continue. To do this:

- Download: https://ollama.com/
- Run an Llama3: `ollama run llama3`

### Unsloth Setup

Unsloth is a tool used for tuning LLM models. For Linux setup, follow the guide on their repo [HERE](https://github.com/unslothai/unsloth). For windows setup, follow these steps:

1. Install CUDA from [HERE](https://developer.nvidia.com/cuda-zone). Next, in your python environment run `pip install torch==2.2.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`

2. Install and open [Visual Studio Installer](https://visualstudio.microsoft.com/downloads/) and select "Desktop Development with C++" under "Workloads". Under "Individual Components", select:

- MSVC v143 - VS 2022 C++ x64/x86 build tools
- Windows 11 SDK
- C++ CMake tools for Windows
- C++ AddressSanitizer

3. Select install to finish setting up Visual Studio 2022 Build Tools

4. Go to [HERE](https://drive.google.com/drive/folders/1aWSFb-ZR8TTIDdRlDBBCh-YvvCxmt6Bc) and download all the files.

5. Create a directory in this project's parent folder called `unsloth_setup`. Move all the files into it and unzip `llvm-5e5a22ca-windows-x64.tar.gz`.

6. In a terminal, run:

```
cd ./unsloth_setup

# Run pwd and replace [PATH_TO_UNSLOTH] in the following commands with the path to the directory.
pwd

set PATH=%PATH%;"[PATH_TO_UNSLOTH]\llvm-5e5a22ca-windows-x64\bin"
set PATH=%PATH%;"[PATH_TO_UNSLOTH]\llvm-5e5a22ca-windows-x64\lib"
```

7. Install the package with the following commands (MAKE SURE YOU DO THESE IN THE LISTED ORDER):

```
pip install triton-2.1.0-cp311-cp311-win_amd64.whl
pip install deepspeed-0.13.1+unknown-py3-none-any.whl
pip install bitsandbytes-0.43.0.dev0-cp311-cp311-win_amd64.whl
```

8. Run `pip install xformers==0.0.24`. Note: you might get issues running training related to Xformers. If you do, run 'pip uninstall xformers' then 'pip install xformers'.

9. If you have a newer RTX 30xx GPU or higher, run `pip install "unsloth[cu121-ampere-torch220] @ git+https://github.com/unslothai/unsloth.git"`, else if you have any other GPU run `pip install "unsloth[cu121-torch220] @ git+https://github.com/unslothai/unsloth.git"`.

If you get no errors, you are done! If you get an error similar to `ERROR: xformers-0.0.24-cp311-cp311-manylinux2014_x86_64.whl is not a supported wheel on this platform.`, follow these steps:

1. In a separate directory, run `git clone https://github.com/unslothai/unsloth.git`

2. Edit the project.toml file to use `https://download.pytorch.org/whl/cu121/xformers-0.0.24-cp311-cp311-win_amd64.whl` on the version you are installing (cu121onlytorch220) for `python_version=='3.11'`.

NOTE: If during training you get an error, you might have to delete this line at line 1561-1562 in `[PATH_TO_CAPSTONE_VENV]\Lib\unsloth\models\llama.py`:

```
for module in target_modules:

    # OTHER CODE

    assert(module in accepted_modules)  # DELETE
    final_modules.append(module)  # DELETE
```

## Drone Manager

The DroneManager class is responsible for controlling the drone based on user input and its environment. This is where all parts of our project come together to communicate with the drone.

The following describes the available functions in the DroneManager class:

**listen(self, model: str, stream: bool=True):** Continuously listen to a microphone and register user input. If a user says **"stop listening"** at any point in a sentence, end listening operations.
- model (str): The model which you would like to use with Ollama.
- stream (bool, default=True): Setting to true will give you the response as it generates, setting to false will only return a response after it is done generating the text.

```
from src.drone_manager import DroneManager

drone = DroneManager()
drone.listen()
```
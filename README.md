# rbpodo-companion
![Ubuntu 24.04](https://img.shields.io/badge/OS-Ubuntu%2024.04-E95420?logo=ubuntu)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker)
![ROS 2 Humble](https://img.shields.io/badge/ROS2-Humble-22314E?logo=ros)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![C++](https://img.shields.io/badge/C++-17-informational?logo=c%2B%2B)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

> [!WARNING]
> This is **not an official Rainbow Robotics repository**.  
> It serves as a community-supported companion project and may not work out-of-the-box in all environments.
> Please test carefully and report issues if you find any.

## Overview

`rbpodo-companion` is a supplementary repository built on top of [rbpodo](https://github.com/RainbowRobotics/rbpodo), designed for real-world applications.
It helps users quickly set up a ROS 2 MoveIt environment and interact with the robot via C++ and Python APIs provided by the rbpodo SDK.

## Getting Started

### Clone the Repository

Make sure to include submodules when cloning:

```bash
git clone --recurse-submodules https://github.com/HobbyLab/rbpodo-companion.git
cd rbpodo-companion
```

> [!WARNING]
> Make sure to clone with `--recurse-submodules`.  
> If you forget, the required `rbpodo` SDK will be missing and builds will fail.

If you already cloned the repository without submodules, fix it with:

```bash
git submodule update --init --recursive
```

## How to Install and Run

You can use this repository in two ways:

1. **With ROS 2** – for MoveIt-based control via Docker
2. **Without ROS 2** – directly using the C++/Python API from `rbpodo`

---

### 1. Using with ROS 2 (Docker-based Control)

Run a container for MoveIt-based control using ROS 2.
The Docker image already includes the `rbpodo` SDK, so you don't need to install it separately.

```bash
# 1. Build Docker image
docker build -t rbpodo-companion:humble .

# 2. Run Docker container with X11 GUI support
docker run -it --rm \
  -e DISPLAY=${DISPLAY} \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  rbpodo-companion:humble

# 3. Launch MoveIt
ros2 launch rbpodo_moveit_config moveit.launch.py \
  model_id:="<ROBOT_MODEL_NAME>" \
  robot_ip:="<YOUR_ROBOT_IP>" \
  use_fake_hardware:=true
```

※ `<ROBOT_MODEL_NAME>`: Robot model name (e.g., `rb3_730es_u`)  
※ `<YOUR_ROBOT_IP>`: Replace with the actual IP address of your robot

---

### 2. Standalone Use (without ROS 2)

If you want to use the `rbpodo` SDK without ROS 2 or Docker,
you can directly install and use the C++ and Python APIs as follows.

#### C++ API Installation

```bash
cd third-party/rbpodo
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
sudo make install
```

#### Python API Installation

This project uses [Poetry](https://python-poetry.org/) for Python dependency and environment management.
It offers better reproducibility and cleaner isolation than traditional `pip` + `venv`.

**Install Poetry (if not already installed):**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Recommended Poetry Setup:**

```bash
# Store virtual environment inside the project folder
poetry config virtualenvs.in-project true

# Add shell support plugin
poetry self add poetry-plugin-shell

# Ensure latest Poetry version
poetry self update
```

**Install project dependencies:**
```bash
poetry install
```

#### Running Python Scripts
After entering the Poetry environment (`poetry shell`), you can run your Python files as usual:
```bash
python <your_python_file>.py
```

Alternatively, without activating the shell, you can use:
```bash
poetry run python <your_python_file>.py
```
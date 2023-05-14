# Placeholder Title
This repository contains both my progress and code for my final year project in wireless networks.

## Installation
To get started with this project, follow the steps below:

**Clone the repository**
- Clone the repository to your local machine using the following command:
```shell
git clone https://github.com/muhd-umer/comm-fyp.git
```

**Create a new virtual environment**
- It is recommended to create a new virtual environment so that updates/downgrades of packages do not break other projects. To create a new virtual environment, run the following command:
```shell
conda env create -f environment.yml
```

- Alternatively, you can use `mamba` (faster than conda) package manager to create a new virtual environment:
```shell
conda install mamba -n base -c conda-forge
mamba env create -f environment.yml
```

**Install the dependencies**
- Activate the newly created environment:
```shell
conda activate fyp
```

- Install PyTorch (Stable 2.0.1):
```shell
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

- Install Ray for Reinforcement Learning:
```shell
pip3 install ray[default]
pip3 install ray[air]
pip3 install ray[tune]
pip3 install ray[rllib]
pip3 install ray[serve]
```

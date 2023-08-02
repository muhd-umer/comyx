<!-- Add logo figure -->
<p align="center">
  <img src=https://raw.githubusercontent.com/muhd-umer/simcomm/main/resources/logo.svg width="500" height="200">
</p>

## SimComm
SimComm is a Python library for simulating wireless communication systems. It uses NumPy and SciPy for numerical computation, and Numba for just-in-time (JIT) compilation. It provides a number of features for simulating wireless communication systems, such as:

- **B5G Features**: SimComm supports a variety of B5G specific features, including STAR-RIS, and NOMA.
- **Channel Models**: SimComm supports including AWGN, Rayleigh fading, and Rician fading.
- **Signal Models**: SimComm supports a variety of signal models, including BPSK, QPSK, and QAM.
- **Performance Metrics**: SimComm can calculate a variety of performance metrics, including sum rate, outage probability.

## To-Do
- [ ] Update documentation
- [ ] Add network optimization support
- [ ] Add Reinforcement Learning (RL) support

## Installation
You can install the latest version of the package using pip:
```shell
pip install simcomm
```

Or you can clone the repository and install the package locally (*Anaconda is recommended*):

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

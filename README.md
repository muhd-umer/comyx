<!-- Add logo figure -->
<p align="center">
  <a href="#null">
    <img src="https://raw.githubusercontent.com/muhd-umer/simcomm/main/resources/logo.svg" alt="Logo" width="500" height="200" style="pointer-events: none; display: block; margin: 0 auto;">
  </a>
</p>

# SimComm
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
$ pip install simcomm
```

Or you can clone the repository and install the package locally in a virtual environment:

**Clone the repository**
- Clone the repository to your local machine using the following command:
```shell
$ git clone https://github.com/muhd-umer/simcomm.git
```

**Install the dependencies**

It is recommended to create a new virtual environment so that updates/downgrades of packages do not break other projects.

- Install the required packages:
```shell
$ pip install -r requirements.txt
```

- Install PyTorch (Stable):
```shell
$ pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

- Install Ray for Reinforcement Learning:
```shell
$ pip install ray[default]
$ pip install ray[air]
$ pip install ray[tune]
$ pip install ray[rllib]
$ pip install ray[serve]
```

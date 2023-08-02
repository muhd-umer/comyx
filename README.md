<p align="center">
  <img src="https://raw.githubusercontent.com/muhd-umer/simcomm/main/resources/logo.svg" width="500" height="200">
</p>

<!-- <p align="center">
    <a href="https://github.com/muhd-umer/simcomm/actions?query=workflow:"build"" alt="build">
        <img src="https://github.com/muhd-umer/simcomm/workflows/build/badge.svg" /></a>
    <a href="https://github.com/muhd-umer/simcomm/releases/" alt="GitHub tag">
        <img src="https://img.shields.io/github/tag/muhd-umer/simcomm?include_prereleases=&sort=semver&color=blue" /></a>
    <a href="https://badge.fury.io/py/simcomm" alt="PyPI version">
        <img src="https://badge.fury.io/py/simcomm.svg" /></a>
    <a href="#license" alt="License">
        <img src="https://img.shields.io/badge/license-MIT-blue?style=flat" /></a>
    <a href="/docs/" alt="view - Documentation">
        <img src="https://img.shields.io/badge/view-docs-blue?style=flat" /></a>
</p>

<p align="center">
    <a href="https://numpy.org/" alt="NumPy">
        <img src="https://img.shields.io/badge/NumPy-%23013243.svg?style=flat&logo=numpy&logoColor=white" /></a>
    <a href="https://scipy.org/" alt="SciPy">
        <img src="https://img.shields.io/badge/SciPy-%230C55A5.svg?style=flat&logo=scipy&logoColor=white" /></a>
    <a href="https://numba.pydata.org/" alt="Numba">
        <img src="https://img.shields.io/badge/Numba-009ed9?style=flat&logo=numba&logoColor=white" /></a>
    <a href="https://pytorch.org/" alt="PyTorch">
        <img src="https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?flat&logo=PyTorch&logoColor=white" /></a>
</p> -->

# SimComm
[![build](https://github.com/muhd-umer/simcomm/workflows/build/badge.svg)](https://github.com/muhd-umer/simcomm/actions?query=workflow:"build")
[![GitHub release](https://img.shields.io/github/release/muhd-umer/simcomm?include_prereleases=&sort=semver&color=blue)](https://github.com/muhd-umer/simcomm/releases/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat)](#license)
[![view - Documentation](https://img.shields.io/badge/view-docs-blue?style=flat)](https://simcomm.readthedocs.io/)
[![NumPy](https://img.shields.io/badge/NumPy-%23013243.svg?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=flat&logo=scipy&logoColor=white)](https://scipy.org/)
[![Numba](https://img.shields.io/badge/Numba-009ed9?style=flat&logo=numba&logoColor=white)](https://numba.pydata.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?flat&logo=PyTorch&logoColor=white)](https://pytorch.org/)

**SimComm** is a Python library for simulating wireless communication systems. It uses **NumPy** and **SciPy** for numerical computation, and **Numba** for just-in-time (JIT) compilation. It provides a number of features for simulating wireless communication systems, such as:

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

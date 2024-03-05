<p align="center">
  <img src="https://raw.githubusercontent.com/muhd-umer/comyx/main/resources/logo.png" width="600">
</p>

<!-- <p align="center">
    <a href="https://github.com/muhd-umer/comyx/actions?query=workflow:"build"" alt="build">
        <img src="https://github.com/muhd-umer/comyx/workflows/build/badge.svg" /></a>
    <a href="https://github.com/muhd-umer/comyx/releases/" alt="GitHub tag">
        <img src="https://img.shields.io/github/tag/muhd-umer/comyx?include_prereleases=&sort=semver&color=blue" /></a>
    <a href="https://badge.fury.io/py/comyx" alt="PyPI version">
        <img src="https://badge.fury.io/py/comyx.svg" /></a>
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

# Comyx: Wireless Network Simulator

[![build](https://github.com/muhd-umer/comyx/workflows/build/badge.svg)](https://github.com/muhd-umer/comyx/actions?query=workflow:"build")
[![GitHub release](https://img.shields.io/github/release/muhd-umer/comyx?include_prereleases=&sort=semver&color=blue)](https://github.com/muhd-umer/comyx/releases/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat)](#license)
[![view - Documentation](https://img.shields.io/badge/view-docs-blue?style=flat)](https://comyx.readthedocs.io/)
[![NumPy](https://img.shields.io/badge/NumPy-%23013243.svg?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=flat&logo=scipy&logoColor=white)](https://scipy.org/)
[![Numba](https://img.shields.io/badge/Numba-009ed9?style=flat&logo=numba&logoColor=white)](https://numba.pydata.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?flat&logo=PyTorch&logoColor=white)](https://pytorch.org/)

**Comyx** is a Python library for simulating wireless communication systems. It uses **NumPy** and **SciPy** for numerical computation, and **Numba** for just-in-time (JIT) compilation. It provides a number of features for simulating wireless communication systems:

- **B5G Features**: Supports a variety of B5G specific features, such as STAR-RIS, and NOMA.
- **Channel Models**: Provides the AWGN, Rayleigh, and Rician fading models.
- **Signal Modulation**: Supports a variety of modulation schemes, such as BPSK, QPSK, and QAM.
- **Performance Metrics**: Can calculate a variety of performance metrics, such as the sum rate, and outage probability.

## To-Do
- [ ] Update documentation
- [ ] Add network optimization support
- [ ] Add Reinforcement Learning (RL) support

## Installation

You can install the latest version of the package using pip:

```shell
pip install comyx
```

*Note: It is recommended to create a new virtual environment so that updates/downgrades of packages do not break other projects.*

Or you can clone the repository along with research code and perform an editable installation:

```shell
git clone https://github.com/muhd-umer/comyx.git
pip install -e .
```

**Reinforcement Learning (RL) Support**

For RL support, you will need to install the following dependencies:

- Install PyTorch (Stable)

    ```shell
    pip install torch torchvision torchaudio
    ```

- Install Ray RLlib

    ```shell
    pip install -U ray[default]  # core, dashboard, cluster launcher
    pip install -U ray[rllib]  # tune, rllib
    ```

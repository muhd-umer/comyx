from typing import Any

import numpy as np
import numpy.typing as npt
from scipy.constants import Boltzmann

from simcomm.utils import pow2db, pow2dbm


def thermal_noise(temperature: float = 300) -> float:
    """Compute the thermal noise.

    Args:
        bandwidth: Bandwidth in Hz.
        temperature: Temperature in Kelvin.

    Returns:
        Thermal noise.
    """
    return Boltzmann * temperature


def get_noise_power(
    bandwidth: float, temperature: float = 300, noise_figure: float = 0
) -> npt.NDArray[np.floating[Any]]:
    """Compute the noise power in dBm.

    Args:
        bandwidth: Bandwidth in Hz.
        temperature: Temperature in Kelvin.
        noise_figure: Noise figure in dB.

    Returns:
        Noise power in dBm.
    """
    if temperature < 0:
        raise ValueError("Temperature must be positive.")
    if bandwidth < 0:
        raise ValueError("Bandwidth must be positive.")

    kT = pow2dbm(thermal_noise(temperature))
    BW = pow2db(bandwidth)
    NF = noise_figure
    return np.asanyarray(kT + NF + BW)

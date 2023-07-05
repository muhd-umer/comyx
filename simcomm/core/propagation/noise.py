"""
Implementation of noise models.
"""

import numpy as np

from simcomm.utils import db2pow, pow2db, dbm2pow, pow2dbm
from scipy.constants import Boltzmann


def thermal_noise(bandwidth, temperature=300):
    """
    Compute the thermal noise.

    Args:
        bandwidth (float): Bandwidth in Hz.
        temperature (float): Temperature in Kelvin.

    Returns:
        float: Thermal noise.
    """
    return Boltzmann * temperature


def get_noise_power(noise_figure, bandwidth, temperature=300):
    """
    Compute the noise power in dBm.

    Args:
        noise_figure (float): Noise figure in dB.
        bandwidth (float): Bandwidth in Hz.
        temperature (float): Temperature in Kelvin.

    Returns:
        float: Noise power in dBm.
    """
    kT = pow2dbm(thermal_noise(bandwidth, temperature))
    BW = pow2db(bandwidth)
    NF = noise_figure
    return kT + NF + BW

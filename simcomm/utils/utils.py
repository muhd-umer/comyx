"""
Common functions for wireless communication simulation.
"""

import numpy as np
from scipy.constants import Boltzmann


def db2pow(db):
    """
    Convert decibels to power.

    Args:
        db (float): Power in decibels.

    Returns:
        float: Power.
    """
    return 10 ** (db / 10)


def pow2db(power):
    """
    Convert power to decibels.

    Args:
        power (float): Power.

    Returns:
        float: Power in decibels.
    """
    return 10 * np.log10(power)


def dbm2pow(dbm):
    """
    Convert decibels relative to 1 milliwatt to power.

    Args:
        dbm (float): Power in decibels relative to 1 milliwatt.

    Returns:
        float: Power in watts.
    """
    return 10 ** ((dbm - 30) / 10)


def pow2dbm(power):
    """
    Convert power to decibels relative to 1 milliwatt.

    Args:
        power (float): Power in watts.

    Returns:
        float: Power in decibels relative to 1 milliwatt.
    """
    return 10 * np.log10(power * 1000)


def distance(pt1, pt2, dim=2):
    """
    Calculate the Euclidean distance between two points.

    Args:
        pt1 (tuple): First point as a tuple of (x, y) or (x, y, z) coordinates.
        pt2 (tuple): Second point as a tuple of (x, y) or (x, y, z) coordinates.
        dim (int): Dimension of the points. Default is 2.

    Returns:
        float: Euclidean distance between the two points.
    """
    if dim == 2:
        return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)
    elif dim == 3:
        return np.sqrt(
            (pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2 + (pt1[2] - pt2[2]) ** 2
        )
    else:
        raise ValueError("Invalid dimension. Must be 2 or 3.")


def get_noise(BW, T, F):
    """
    Calculates the total noise power in a system.

    Args:
        BW (float): The bandwidth of the system in Hz.
        T (float): The temperature of the system in Kelvin.
        F (float): The noise figure of the system in dB.

    Returns:
        float: The total noise power in dBm.
    """
    k = Boltzmann
    kT = 10 * np.log10(k * T)
    BW = 10 * np.log10(BW)
    N = kT + BW + F

    return N


def snr(signal_power, noise_power):
    """
    Calculate the signal-to-noise ratio (SNR) in decibels.

    Args:
        signal_power (float): Signal power in watts.
        noise_power (float): Noise power in watts.

    Returns:
        float: SNR in decibels.
    """
    return 10 * np.log10(signal_power / noise_power)

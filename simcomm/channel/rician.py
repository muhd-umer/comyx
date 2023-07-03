"""
Implementation of Rician fading channel.
"""

import numpy as np

from .rayleigh import *


def rician_fading(K, P_los, n=1, link=True):
    """
    Generate the Rician fading channel coefficients.

    Args:
        K: The Rician K-factor.
        P_los: The power of the line-of-sight component.
        n: The number of samples to generate. Defaults to 1.

    Returns:
        A NumPy array of complex numbers representing the fading coefficients.
    """

    s = np.sqrt(K / (K + 1) * P_los)  # Non-centrality parameter
    sigma = P_los / np.sqrt(2 * (K + 1))  # Standard deviation
    if link:
        los = np.sqrt(
            (np.random.normal(s, sigma) ** 2) + 1j * (np.random.normal(0, sigma) ** 2)
        )
        nlos = rayleigh_fading(n)
        h = np.sqrt(K / (K + 1)) * los + np.sqrt(1 / (K + 1)) * nlos
    else:
        h = np.sqrt(
            (np.random.normal(s, sigma) ** 2) + 1j * (np.random.normal(0, sigma) ** 2)
        )
    return h

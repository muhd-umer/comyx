"""
Implementation of Rayleigh fading channel.
"""

import numpy as np


def rayleigh_fading(n=1):
    """
    Generate the Rayleigh fading channel coefficients.

    Args:
        n: The number of samples to generate. Defaults to 1.

    Returns:
        A NumPy array of complex numbers representing the fading coefficients.
    """

    h = (np.random.randn(n) + 1j * np.random.randn(n)) / np.sqrt(2)
    return h

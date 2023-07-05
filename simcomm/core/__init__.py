from .fading import *
from .propagation import *
import numpy as np


def generate_channel(small_scale_fading, distance, eta):
    """
    Generates the channel coefficients.

    Args:
        small_scale_fading: The small scale fading coefficients.
        distance: The distance between the transmitter and receiver.
        eta: The path loss exponent.

    Returns:
        A NumPy array of complex numbers representing the channel coefficients.
    """
    large_scale_fading = np.sqrt(distance ** (-eta))
    h = large_scale_fading * small_scale_fading

    return h

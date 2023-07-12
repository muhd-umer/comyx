from .fading import *
from .propagation import *
from ..utils import db2pow
import numpy as np


def generate_channel(small_scale_fading, distance, frequency, eta, sigma):
    """
    Generates the channel coefficients.

    Args:
        small_scale_fading: The small scale fading coefficients.
        distance: The distance between the transmitter and receiver.
        frequency: The frequency of the signal.
        eta: The path loss exponent.
        sigma: The shadow fading standard deviation.

    Returns:
        A NumPy array of complex numbers representing the channel coefficients.
    """
    large_scale_fading = np.sqrt(
        db2pow(
            get_pathloss(
                "log-distance", distance, frequency, d_break=10, alpha=eta, sigma=sigma
            )
            * -1
        )
    )
    h = large_scale_fading * small_scale_fading

    return h

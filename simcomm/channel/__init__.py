import numpy as np

from .rayleigh import *
from .rician import *


def get_fading(type, *args, **kwargs):
    """
    Generates the fading channel coefficients.

    Args:
        type: The type of the fading.
        distance: The distance between the transmitter and receiver.
        eta: The path loss exponent.
        *args: The arguments to pass to the channel generator.
        **kwargs: The keyword arguments to pass to the channel generator.

    Returns:
        A NumPy array of complex numbers representing the fading coefficients.
    """

    if type == "rayleigh":
        small_scale_fading = rayleigh_fading(*args, **kwargs)
    elif type == "rician":
        small_scale_fading = rician_fading(*args, **kwargs)
    else:
        raise NotImplementedError(f"Channel type {type} is not implemented")

    return small_scale_fading


def get_channel(small_scale_fading, distance, eta):
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

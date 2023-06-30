import numpy as np

from .rayleigh import *
from .rician import *


def generate_channel(channel_type, distance, eta, *args, **kwargs):
    """
    Generates the fading channel coefficients.

    Args:
        channel_type: The type of the channel.
        distance: The distance between the transmitter and receiver.
        eta: The path loss exponent.
        *args: The arguments to pass to the channel generator.
        **kwargs: The keyword arguments to pass to the channel generator.

    Returns:
        A NumPy array of complex numbers representing the fading coefficients.
    """

    if channel_type == "rayleigh":
        small_scale_fading = rayleigh_fading(*args, **kwargs)
    elif channel_type == "rician":
        small_scale_fading = rician_fading(*args, **kwargs)
    else:
        raise NotImplementedError(f"Channel type {channel_type} is not implemented")

    large_scale_fading = np.sqrt(distance**eta)
    channel_gain = np.abs(small_scale_fading / large_scale_fading) ** 2

    return channel_gain

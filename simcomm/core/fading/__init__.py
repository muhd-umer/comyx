from .rayleigh import *
from .rician import *


def get_fading(type, *args, **kwargs):
    """
    Generates the fading channel coefficients.

    Args:
        type: The type of the fading. ("rayleigh", "rician")
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

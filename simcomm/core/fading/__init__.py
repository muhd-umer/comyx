from .rayleigh import *
from .rician import *


def get_multipath_fading(type, size, *args, **kwargs):
    """
    Generates the multipath fading coefficients.

    Args:
        type: The type of the fading. ("rayleigh", "rician")
        size: The number of fading coefficients to generate.
        library: The library to use for generating the fading coefficients.

    Rayleigh Args:
        sigma: The scale parameter of the Rayleigh distribution.

    Rician Args:
        K: The shape parameter of the Rician distribution.
        sigma: The scale parameter of the Rician distribution.

    Returns:
        Channel gains.
    """

    if type == "rayleigh":
        distribution = Rayleigh(*args, **kwargs)
        coefficients = distribution.generate_coefficients(size=size)

    elif type == "rician":
        distribution = Rician(*args, **kwargs)
        coefficients = distribution.generate_coefficients(size=size)

    else:
        raise NotImplementedError(f"Channel type {type} is not implemented")

    return coefficients

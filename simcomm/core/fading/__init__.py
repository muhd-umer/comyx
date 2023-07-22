from .rayleigh import *
from .rician import *


def get_rvs(type, shape, *args, **kwargs):
    """
    Generates random variables from a distribution.

    Args:
        type: The type of the fading. ("rayleigh", "rician")
        shape: The number of fading coefficients to generate.
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
        coefficients = distribution.generate_samples(size=shape)

    elif type == "rician":
        distribution = Rician(*args, **kwargs)
        coefficients = distribution.generate_samples(size=shape)

    else:
        raise NotImplementedError(f"Channel type {type} is not implemented")

    return coefficients

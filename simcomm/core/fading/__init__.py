from typing import Any, Tuple, Union

import numpy as np
import numpy.typing as npt

from .rayleigh import Rayleigh
from .rician import Rician


def get_rvs(
    type: str, shape: Union[int, Tuple[int, ...]], *args, **kwargs
) -> npt.NDArray[np.floating[Any]]:
    """
    Generates random variables from a distribution.

    Args:
        type (str): The type of the fading. ("rayleigh", "rician")
        shape (int or tuple of ints): The number of fading coefficients to generate.

    Rayleigh Args:
        sigma (float): The scale parameter of the Rayleigh distribution.

    Rician Args:
        K (float): Rician K-factor in dB.
        sigma (float): The scale parameter of the Rician distribution.

    Returns:
        Channel gains.
    """

    if type == "rayleigh":
        distribution = Rayleigh(*args, **kwargs)
        coefficients = distribution.get_samples(size=shape)

    elif type == "rician":
        distribution = Rician(*args, **kwargs)
        coefficients = distribution.get_samples(size=shape)

    else:
        raise NotImplementedError(f"Channel type {type} is not implemented")

    return coefficients


__all__ = ["get_rvs", "Rayleigh", "Rician"]

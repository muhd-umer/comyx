from __future__ import annotations

from typing import Any, Tuple, Union

import numpy as np
import numpy.typing as npt

from .nakagami import Nakagami
from .rayleigh import Rayleigh
from .rician import Rician

NDArrayFloat = npt.NDArray[np.floating[Any]]


def get_rvs(
    type: str, shape: Union[int, Tuple[int, ...]], *args, **kwargs
) -> NDArrayFloat:
    """Generates random variables from a distribution.

    Args:
        type: Type of the fading. ("rayleigh", "rician")
        shape: Number of fading samples to generate.

    Rayleigh Args:
        sigma: Scale parameter of the Rayleigh distribution.

    Rician Args:
        K: Rician K-factor in dB.
        sigma: Scale parameter of the Rician distribution.

    Nakagami Args:
        m: Shape parameter of the Nakagami distribution.
        omega: Scale parameter of the Nakagami distribution.

    Returns:
        Channel gains.
    """

    if type == "rayleigh":
        distribution = Rayleigh(*args, **kwargs)
        samples = distribution.get_samples(size=shape)

    elif type == "rician":
        distribution = Rician(*args, **kwargs)
        samples = distribution.get_samples(size=shape)

    elif type == "nakagami":
        distribution = Nakagami(*args, **kwargs)
        samples = distribution.get_samples(size=shape)

    else:
        raise NotImplementedError(f"Channel type {type} is not implemented")

    return samples


__all__ = ["get_rvs"]

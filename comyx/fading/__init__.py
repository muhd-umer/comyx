from __future__ import annotations

from typing import Any, Tuple, Union

import numpy as np
import numpy.typing as npt

from .nakagami import Nakagami
from .rayleigh import Rayleigh
from .rician import Rician

NDArrayFloat = npt.NDArray[np.floating[Any]]
NDArrayComplex = npt.NDArray[np.complexfloating[Any, Any]]


def get_rvs(
    shape: Union[int, Tuple[int, ...]], type: str, *args, **kwargs
) -> NDArrayComplex:
    """Generates random variables from a distribution.

    Rayleigh
        - ``sigma``– Scale parameter of the Rayleigh distribution.

    Rician
        - ``K`` – Rician K-factor in dB.
        - ``sigma`` – Scale parameter of the Rician distribution.

    Nakagami
        - ``m`` – Shape parameter of the Nakagami distribution.
        - ``omega`` – Scale parameter of the Nakagami distribution.

    Args:
        shape: Number of fading samples to generate.
        type: Type of the fading. ("rayleigh", "rician")

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

    return np.array(
        samples * np.exp(1j * np.random.uniform(0, 2 * np.pi, shape)), dtype=complex
    )


__all__ = ["get_rvs", "Rayleigh", "Rician", "Nakagami"]

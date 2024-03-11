from __future__ import annotations

import hashlib
from typing import Any, List, Union

import numpy as np
import numpy.typing as npt
import pandas as pd
import scipy as sp
from scipy.special import i0, i1

NDArrayFloat = npt.NDArray[np.floating[Any]]
NDArraySigned = npt.NDArray[np.signedinteger[Any]]


def db2pow(db: Union[float, NDArrayFloat]) -> NDArrayFloat:
    """Convert power in decibels to watts.

    Args:
        db: Power in decibels.

    Returns:
        Power in watts.
    """
    return np.array(10 ** (db / 10))


def pow2db(power: Union[float, NDArrayFloat]) -> NDArraySigned:
    """Convert power in watts to decibels.

    Args:
        power: Power in watts.

    Returns:
        Power in decibels.
    """
    return np.array(10 * np.log10(power))


def dbm2pow(dbm: Union[float, NDArrayFloat]) -> NDArrayFloat:
    """Convert decibels relative to 1 milliwatt to watts.

    Args:
        dbm: Power in decibels relative to 1 milliwatt.

    Returns:
        Power in watts.
    """
    return np.array(10 ** ((dbm - 30) / 10))


def pow2dbm(power: Union[float, NDArrayFloat]) -> NDArraySigned:
    """Convert power in watts to decibels relative to 1 milliwatt.

    Args:
        pow: Power in watts.

    Returns:
        Power in decibels relative to 1 milliwatt.
    """
    return np.array(10 * np.log10(power * 1000))


def get_distance(pt1: List[Any], pt2: List[Any]) -> float:
    """Calculate the Euclidean distance between two points.

    Points must have the same dimension and be a list of length 2 or 3.

    Example usage:
        >>> get_distance([0, 0], [1, 1])
        1.4142135623730951
        >>> get_distance([0, 0, 0], [1, 1, 1])
        1.7320508075688772

    Args:
        pt1: The first point.
        pt2: The second point.

    Returns:
        The Euclidean distance between the two points.
    """
    assert len(pt1) == len(pt2), ValueError("Points must have the same dimension.")
    if len(pt1) == 2:
        return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)
    elif len(pt1) == 3:
        return np.sqrt(
            (pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2 + (pt1[2] - pt2[2]) ** 2
        )
    else:
        raise ValueError("Invalid dimension. Must be 2 or 3.")


def rolling_mean(data: NDArrayFloat, window_size: int) -> NDArrayFloat:
    """Compute the rolling mean of a curve.

    Args:
        data: The curve to filter.
        window_size: The size of the window.

    Returns:
        Data list with the rolling mean applied.
    """

    filtered_curve = pd.Series(data).rolling(window_size).mean()

    return np.array(filtered_curve.tolist())


def qfunc(x: Union[float, NDArrayFloat]) -> NDArrayFloat:
    """Compute the Q function.

    Args:
        x: Input to the Q function.

    Returns:
        Q function computed at x.
    """
    return 0.5 * sp.special.erfc(x / np.sqrt(2))


def inverse_qfunc(x: Union[float, NDArrayFloat]) -> NDArrayFloat:
    """Inverse Q function.

    Args:
        x: Input to the inverse Q function.

    Returns:
        Inverse Q function computed at x.
    """
    return np.sqrt(2) * sp.special.erfcinv(2 * x)


def laguerre(x: Union[float, NDArrayFloat], n: float) -> Union[float, NDArrayFloat]:
    """Compute the Laguerre polynomial.

    Args:
        x: Input to the Laguerre polynomial.
        n: The order of the Laguerre polynomial.

    Returns:
        Laguerre polynomial computed at x and order n.
    """

    if n == 0:
        return 1
    elif n == 1 / 2:
        return np.exp(x / 2) * ((1 - x) * i0(-x / 2) - x * i1(-x / 2))
    elif n == 1:
        return 1 - x
    else:
        return ((2 * n - 1 - x) * laguerre(x, n - 1) - (n - 1) * laguerre(x, n - 2)) / n


def wrap_to_2pi(theta: NDArrayFloat) -> NDArrayFloat:
    """Wrap an angle to the interval [0, 2 * pi].

    Args:
        theta: The angle to wrap.

    Returns:
        The wrapped angle.
    """

    return np.mod(theta, 2 * np.pi)


def ensure_list(arg, length) -> List[Any]:
    """Ensure that the argument is a list of desired length.

    Args:
        arg: The argument to check.
        length: The desired length of the list.

    Returns:
        Argument repeated length times if it is not a list, otherwise the
        argument itself.
    """
    return arg if isinstance(arg, list) else [arg for _ in range(length)]


def generate_seed(identifier: str) -> int:
    """Generate a seed from an identifier.

    Seed is generated using the MD5 hash of the identifier. The hash is then
    converted to an integer and the modulo operation is applied to ensure the
    seed fits into a 32-bit integer.

    Args:
        identifier: The identifier to hash.

    Returns:
        A seed for random number generation.
    """

    hash_object = hashlib.md5(identifier.encode())
    return int(hash_object.hexdigest(), 16) % (2**32 - 1)


__all__ = [
    "db2pow",
    "pow2db",
    "dbm2pow",
    "pow2dbm",
    "get_distance",
    "rolling_mean",
    "qfunc",
    "inverse_qfunc",
    "laguerre",
    "wrap_to_2pi",
    "ensure_list",
    "generate_seed",
]

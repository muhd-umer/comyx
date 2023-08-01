from typing import Any, List, Union

import numpy as np
import numpy.typing as npt
import pandas as pd
import scipy as sp
from scipy.special import i0, i1


def db2pow(
    db: Union[float, npt.NDArray[np.floating[Any]]]
) -> Union[float, npt.NDArray[np.floating[Any]]]:
    """Convert decibels to power.

    Args:
        db (float or ndarray): Power in decibels.

    Returns:
        pow (float or ndarray): Power.
    """
    return 10 ** (db / 10)


def pow2db(
    power: Union[float, npt.NDArray[np.floating[Any]]]
) -> Union[float, npt.NDArray[np.signedinteger[Any]]]:
    """Convert power to decibels.

    Args:
        power (float or ndarray): Power in watts.

    Returns:
        db (float or ndarray): Power in decibels.
    """
    return 10 * np.log10(power)


def dbm2pow(
    dbm: Union[float, npt.NDArray[np.floating[Any]]]
) -> Union[float, npt.NDArray[np.floating[Any]]]:
    """Convert decibels relative to 1 milliwatt to power.

    Args:
        dbm (float or ndarray): Power in decibels relative to 1 milliwatt.

    Returns:
        pow (float or ndarray): Power in watts.
    """
    return 10 ** ((dbm - 30) / 10)


def pow2dbm(
    power: Union[float, npt.NDArray[np.floating[Any]]]
) -> Union[float, npt.NDArray[np.signedinteger[Any]]]:
    """Convert power to decibels relative to 1 milliwatt.

    Args:
        pow (float or ndarray): Power in watts.

    Returns:
        dbm (float or ndarray): Power in decibels relative to 1 milliwatt.
    """
    return 10 * np.log10(power * 1000)


def get_distance(pt1: List[Any], pt2: List[Any], dim: int = 2) -> float:
    """Calculate the Euclidean distance between two points.

    Args:
        pt1 (list): First point as a list of [x, y] or [x, y, z] coordinates.
        pt2 (list): Second point as a list of [x, y] or [x, y, z] coordinates.
        dim (int): Dimension of the points. Default is 2.

    Returns:
        distance (float): Euclidean distance between the two points.
    """
    if dim == 2:
        return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)
    elif dim == 3:
        return np.sqrt(
            (pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2 + (pt1[2] - pt2[2]) ** 2
        )
    else:
        raise ValueError("Invalid dimension. Must be 2 or 3.")


def rolling_mean(data: npt.NDArray[np.floating[Any]], window_size: int) -> List[Any]:
    """Compute the rolling mean of a curve.

    Args:
        data (ndarray): The curve to filter.
        window_size (int): The size of the window.

    Returns:
        list: The filtered curve.
    """

    filtered_curve = pd.Series(data).rolling(window_size).mean()

    return filtered_curve.tolist()


def randomize_user_pos(
    bs_pos: List[Any],
    user_pos: List[Any],
    edge_idx: int,
    r_min: List[Any] = [30],
    r_max: List[Any] = [100],
) -> List[Any]:
    """Randomize the positions of the users in the network, except for the edge user.

    Args:
        bs_pos (list): A list of the positions of the base stations.
        user_pos (list): A list of the positions of the users.
        edge_idx (int): The index of the edge user.
        r_min (list): A list of minimum distances between the users and the base stations. Defaults to [30].
        r_max (list): A list of maximum distances between the users and the base stations. Defaults to [100].

    Returns:
        list: A list of the positions of the users.
    """
    for i in range(len(user_pos)):
        if i == edge_idx:
            continue
        bs_idx = np.argmin(np.linalg.norm(bs_pos - user_pos[i], axis=1))
        rm = r_min[i] if len(r_min) > i else r_min[-1]
        rM = r_max[i] if len(r_max) > i else r_max[-1]
        r = np.random.uniform(rm, rM)
        theta = np.random.uniform(0, 2 * np.pi)
        user_pos[i] = bs_pos[bs_idx] + r * np.array([np.cos(theta), np.sin(theta), 0])
    return user_pos


def qfunc(x: Union[float, npt.NDArray[np.floating[Any]]]) -> float:
    """Compute the Q function.

    Args:
        x (ndarray): Input to the Q function.

    Returns:
        qfunc (ndarray): The Q function.
    """
    return 0.5 * sp.special.erfc(x / np.sqrt(2))


def inverse_qfunc(x: Union[float, npt.NDArray[np.floating[Any]]]) -> float:
    """Inverse Q function.

    Args:
        x (ndarray): Input to the inverse Q function.

    Returns:
        inverse_qfunc (ndarray): The inverse Q function.
    """
    return np.sqrt(2) * sp.special.erfcinv(2 * x)


def laguerre(
    x: Union[float, npt.NDArray[np.floating[Any]]], n: float
) -> Union[float, npt.NDArray[np.floating[Any]]]:
    """Compute the Laguerre polynomial.

    Args:
        x (float or ndarray): Input to the Laguerre polynomial.
        n (float): The order of the Laguerre polynomial.

    Returns:
        laguerre (float or ndarray): The Laguerre polynomial.
    """

    if n == 0:
        return 1
    elif n == 1 / 2:
        return np.exp(x / 2) * ((1 - x) * i0(-x / 2) - x * i1(-x / 2))
    elif n == 1:
        return 1 - x
    else:
        return ((2 * n - 1 - x) * laguerre(x, n - 1) - (n - 1) * laguerre(x, n - 2)) / n


def wrapTo2Pi(theta: npt.NDArray[np.floating[Any]]) -> npt.NDArray[np.floating[Any]]:
    """Wrap an angle to the interval [0, 2 * pi].

    Args:
        theta (ndarray): The angle to wrap.

    Returns:
        wrapped_theta (ndarray): The wrapped angle.
    """

    return np.mod(theta, 2 * np.pi)

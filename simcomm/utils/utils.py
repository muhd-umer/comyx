import numpy as np
import pandas as pd
import scipy as sp
from scipy.special import i0, i1


def db2pow(db: float) -> float:
    """Convert decibels to power.

    Args:
        db: Power in decibels.

    Returns:
        Power.
    """
    return 10 ** (db / 10)


def pow2db(power: float) -> float:
    """Convert power to decibels.

    Args:
        power: Power.

    Returns:
        Power in decibels.
    """
    return 10 * np.log10(power)


def dbm2pow(dbm: float) -> float:
    """Convert decibels relative to 1 milliwatt to power.

    Args:
        dbm: Power in decibels relative to 1 milliwatt.

    Returns:
        Power in watts.
    """
    return 10 ** ((dbm - 30) / 10)


def pow2dbm(power: float) -> float:
    """Convert power to decibels relative to 1 milliwatt.

    Args:
        power: Power in watts.

    Returns:
        Power in decibels relative to 1 milliwatt.
    """
    return 10 * np.log10(power * 1000)


def get_distance(pt1: tuple, pt2: tuple, dim: int = 2) -> float:
    """Calculate the Euclidean distance between two points.

    Args:
        pt1: First point as a tuple of (x, y) or (x, y, z) coordinates.
        pt2: Second point as a tuple of (x, y) or (x, y, z) coordinates.
        dim: Dimension of the points. Default is 2.

    Returns:
        Euclidean distance between the two points.
    """
    if dim == 2:
        return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)
    elif dim == 3:
        return np.sqrt(
            (pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2 + (pt1[2] - pt2[2]) ** 2
        )
    else:
        raise ValueError("Invalid dimension. Must be 2 or 3.")


def rolling_mean(data: list, window_size: int) -> list:
    """Compute the rolling mean of a curve.

    Args:
        data: The curve to filter.
        window_size: The size of the window to use for the rolling mean.

    Returns:
        The filtered curve.
    """

    filtered_curve = pd.Series(data).rolling(window_size).mean()

    return filtered_curve.tolist()


def randomize_user_pos(
    bs_pos: np.ndarray,
    user_pos: np.ndarray,
    edge_idx: int,
    r_min: list = [30],
    r_max: list = [100],
) -> np.ndarray:
    """Randomize the user positions in the network except the edge user.

    Args:
        bs_pos: Position of the base stations.
        user_pos: Position of the users.
        edge_idx: Index of the edge user.
        r_min: List of minimum distances between the users and the base stations. Defaults to [30].
        r_max: List of maximum distances between the users and the base stations. Defaults to [100].

    Returns:
        Position of the users.
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


def qfunc(x: float) -> float:
    """Compute the Q function.

    Args:
        x: The input.

    Returns:
        The output.
    """
    return 0.5 * sp.special.erfc(x / np.sqrt(2))


def inverse_qfunc(x: float) -> float:
    """Compute the inverse Q function.

    Args:
        x: The input.

    Returns:
        The output.
    """
    return np.sqrt(2) * sp.special.erfcinv(2 * x)


def laguerre(x: float, n: float) -> float:
    """Compute the Laguerre polynomial of degree n.

    Args:
        x: The input.
        n: The degree of the polynomial.

    Returns:
        The output.
    """

    if n == 0:
        return 1
    elif n == 1 / 2:
        return np.exp(x / 2) * ((1 - x) * i0(-x / 2) - x * i1(-x / 2))
    elif n == 1:
        return 1 - x
    else:
        return ((2 * n - 1 - x) * laguerre(x, n - 1) - (n - 1) * laguerre(x, n - 2)) / n


def fix_range(phase: np.ndarray) -> np.ndarray:
    """Convert phase to the range [-pi, pi].

    Args:
        phase: The phase array.

    Returns:
        The phase array in the range [-pi, pi].
    """
    phi = np.where(phase > np.pi, phase - 2 * np.pi, phase)
    return np.where(phi < -np.pi, phi + 2 * np.pi, phi)

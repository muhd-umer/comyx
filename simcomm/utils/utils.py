"""
Common functions for wireless communication simulation.
"""

import numpy as np
import pandas as pd
from scipy.constants import Boltzmann


def db2pow(db):
    """
    Convert decibels to power.

    Args:
        db (float): Power in decibels.

    Returns:
        float: Power.
    """
    return 10 ** (db / 10)


def pow2db(power):
    """
    Convert power to decibels.

    Args:
        power (float): Power.

    Returns:
        float: Power in decibels.
    """
    return 10 * np.log10(power)


def dbm2pow(dbm):
    """
    Convert decibels relative to 1 milliwatt to power.

    Args:
        dbm (float): Power in decibels relative to 1 milliwatt.

    Returns:
        float: Power in watts.
    """
    return 10 ** ((dbm - 30) / 10)


def pow2dbm(power):
    """
    Convert power to decibels relative to 1 milliwatt.

    Args:
        power (float): Power in watts.

    Returns:
        float: Power in decibels relative to 1 milliwatt.
    """
    return 10 * np.log10(power * 1000)


def get_distance(pt1, pt2, dim=2):
    """
    Calculate the Euclidean distance between two points.

    Args:
        pt1 (tuple): First point as a tuple of (x, y) or (x, y, z) coordinates.
        pt2 (tuple): Second point as a tuple of (x, y) or (x, y, z) coordinates.
        dim (int): Dimension of the points. Default is 2.

    Returns:
        float: Euclidean distance between the two points.
    """
    if dim == 2:
        return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)
    elif dim == 3:
        return np.sqrt(
            (pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2 + (pt1[2] - pt2[2]) ** 2
        )
    else:
        raise ValueError("Invalid dimension. Must be 2 or 3.")


def rolling_mean(data, window_size):
    """
    Compute the rolling mean of a curve.

    Args:
        data (list): The curve to filter.
        window_size (int): The size of the window to use for the rolling mean.

    Returns:
        list: The filtered curve.
    """

    filtered_curve = pd.Series(data).rolling(window_size).mean()

    return filtered_curve


def randomize_user_pos(bs_pos, user_pos, edge_idx, r_min=[30], r_max=[100]):
    """
    Randomize the user positions in the network except the edge user.

    Args:
        bs_pos (numpy.ndarray): Position of the base stations.
        user_pos (numpy.ndarray): Position of the users.
        edge_idx (int): Index of the edge user.
        r_min (list): List of minimum distances between the users and the base stations. Defaults to [30].
        r_max (list): List of maximum distances between the users and the base stations. Defaults to [100].

    Returns:
        numpy.ndarray: Position of the users.
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

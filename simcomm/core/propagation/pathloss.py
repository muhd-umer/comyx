from typing import Any, Union

import numpy as np
import numpy.typing as npt

from ...utils import pow2db


def get_pathloss(
    type: str,
    distance: float,
    frequency: float,
    *args,
    **kwargs,
) -> npt.NDArray[np.floating[Any]]:
    """Get path loss in dB.

    Args:
        type (str): Path loss model type. ("free-space", "log-distance")
        distance (float): Distance between transmitter and receiver.
        frequency (float): Frequency of the signal.
        *args: Positional arguments for the path loss model.
        **kwargs: Keyword arguments for the path loss model.

    Returns:
        Path loss in dB.

    - FSPL Args:
        - alpha (float): Path loss exponent.
        - p0 (float): Reference path loss at 1m.

    - Log Distance Args:
        - d0 (float): The breakpoint distance.
        - alpha (float): The path loss exponent.
        - sigma (float): The shadow fading standard deviation.

    """
    if type == "free-space":
        return free_space(distance, *args, **kwargs)
    if type == "friis":
        return friis(distance, frequency)
    elif type == "log-distance":
        return log_distance(distance, frequency, *args, **kwargs)
    else:
        raise NotImplementedError(f"Path loss model {type} not implemented.")


def free_space(
    distance: float, alpha: float, p0: float
) -> npt.NDArray[np.floating[Any]]:
    """Free space path loss model.

    Args:
        distance (float): Distance between transmitter and receiver.
        alpha (float): Path loss exponent.
        p0 (float): Reference path loss at 1m.

    Returns:
        loss (array_like): Path loss in dB.
    """
    loss = pow2db(distance**alpha) + p0
    return np.array(loss)


def friis(distance: float, frequency: float) -> npt.NDArray[np.floating[Any]]:
    """Friis path loss model.

    Args:
        distance (float): Distance between transmitter and receiver.
        frequency (float): Frequency of the signal.

    Returns:
        loss (float): Path loss in dB.
    """
    lambda_ = 3e8 / frequency
    loss = 20 * np.log10(4 * np.pi * distance / lambda_)
    return loss


def log_distance(
    distance: float, frequency: float, d0: float, alpha: float, sigma: float
) -> npt.NDArray[np.floating[Any]]:
    """Log distance path loss model.

    Args:
        distance (float): Distance between transmitter and receiver.
        frequency (float): Frequency of the signal.
        d0 (float): Break distance.
        alpha (float): Path loss exponent.
        sigma (float): Shadow fading standard deviation.

    Returns:
        loss (float): Path loss in dB.
    """
    lambda_ = 3e8 / frequency
    loss_break = 20 * np.log10(4 * np.pi * d0 / lambda_)
    loss = (
        loss_break + 10 * alpha * np.log10(distance / d0) + np.random.normal(0, sigma)
    )
    return loss

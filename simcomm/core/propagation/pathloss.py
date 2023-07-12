"""
Implementation of path loss models.
"""

import numpy as np


def get_pathloss(type, distance, frequency, *args, **kwargs):
    """
    Get path loss in dB.

    Args:
        type: Path loss model type. ("free-space", "log-distance")
        distance: Distance between transmitter and receiver.
        frequency: Frequency of the signal.

    Optional Args:
        d_break: The breakpoint distance.
        eta: The path loss exponent.
        sigma: The shadow fading standard deviation.

    Returns:
        Path loss in dB.
    """
    if type == "free-space":
        return free_space(distance, frequency)
    elif type == "log-distance":
        return log_distance(distance, frequency, *args, **kwargs)
    else:
        raise NotImplementedError(f"Path loss model {type} not implemented.")


def free_space(distance, frequency):
    """
    Free space path loss model.

    Args:
        distance: Distance between transmitter and receiver.
        frequency: Frequency of the signal.

    Returns:
        Path loss in dB.
    """
    lambda_ = 3e8 / frequency
    loss = 20 * np.log10(4 * np.pi * distance / lambda_)
    return loss


def log_distance(distance, frequency, d_break, alpha, sigma):
    """
    Log distance path loss model.

    Args:
        distance: Distance between transmitter and receiver.
        frequency: Frequency of the signal.
        d_break: Break distance.
        alpha: Path loss exponent.
        sigma: Shadow fading standard deviation.

    Returns:
        Path loss in dB.
    """
    lambda_ = 3e8 / frequency
    loss_break = 20 * np.log10(4 * np.pi * d_break / lambda_)
    loss = (
        loss_break
        + 10 * alpha * np.log10(distance / d_break)
        + np.random.normal(0, sigma)
    )
    return loss

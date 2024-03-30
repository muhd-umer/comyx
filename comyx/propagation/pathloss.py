from __future__ import annotations

from typing import Any

import numpy as np
import numpy.typing as npt

from ..utils import pow2db

NDArrayFloat = npt.NDArray[np.floating[Any]]


def get_pathloss(
    distance: float,
    type: str,
    frequency: float,
    *args,
    **kwargs,
) -> NDArrayFloat:
    """Get path loss in dB.

    Reference:
        alpha: Path loss exponent.
        p0: Reference path loss at 1m.

    Log Distance:
        d0: The breakpoint distance.
        alpha: The path loss exponent.
        sigma: The shadow fading standard deviation.

    Args:
        distance: Distance between transmitter and receiver.
        type: Path loss model type. ("reference", "friis", "log-distance")
        frequency: Frequency of the signal.
        *args: Positional arguments for the path loss model.
        **kwargs: Keyword arguments for the path loss model.

    Returns:
        Path loss in dB.

    """
    if type == "reference":
        return reference(distance, *args, **kwargs)
    if type == "friis":
        return friis(distance, frequency)
    elif type == "log-distance":
        return log_distance(distance, frequency, *args, **kwargs)
    else:
        raise NotImplementedError(f"Path loss model {type} not implemented.")


def reference(distance: float, alpha: float, p0: float) -> NDArrayFloat:
    """General path loss model.

    Args:
        distance: Distance between transmitter and receiver.
        alpha: Path loss exponent.
        p0: Reference path loss at 1m.

    Returns:
        loss: Path loss in dB.
    """
    loss = p0 + 10 * alpha * np.log10(distance)
    return np.array(loss)


def friis(distance: float, frequency: float) -> NDArrayFloat:
    """Friis path loss model.

    Args:
        distance: Distance between transmitter and receiver.
        frequency: Frequency of the signal.

    Returns:
        loss: Path loss in dB.
    """
    lambda_ = 3e8 / frequency
    loss = 20 * np.log10(4 * np.pi * distance / lambda_)
    return loss


def log_distance(
    distance: float, frequency: float, d0: float, alpha: float, sigma: float
) -> NDArrayFloat:
    """Log distance path loss model.

    Args:
        distance: Distance between transmitter and receiver.
        frequency: Frequency of the signal.
        d0: Break distance.
        alpha: Path loss exponent.
        sigma: Shadow fading standard deviation.

    Returns:
        loss: Path loss in dB.
    """
    lambda_ = 3e8 / frequency
    loss_break = 20 * np.log10(4 * np.pi * d0 / lambda_)
    loss = (
        loss_break + 10 * alpha * np.log10(distance / d0) + np.random.normal(0, sigma)
    )
    return loss


__all__ = ["get_pathloss"]

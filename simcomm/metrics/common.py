from typing import List, Union

import numpy as np
import numpy.typing as npt


def get_outage(
    instantaneous_rate: Union[float, List[float]], target_rate: float
) -> Union[int, List[int]]:
    """Compute the outage probability.

    Args:
        instantaneous_rate (float or list): The instantaneous rate(s) of the link(s).
        target_rate (float): The target rate of the link.

    Returns:
        outage (int or list): The outage probability of the link(s).
    """
    if isinstance(instantaneous_rate, list):
        outage = [1 if rate < target_rate else 0 for rate in instantaneous_rate]
    else:
        outage = 1 if instantaneous_rate < target_rate else 0

    return outage


def get_snr(signal_power: Union[float, npt.NDArray[np.floating]], noise_power: float):
    """Calculate the signal-to-noise ratio (SNR) in decibels.

    Args:
        signal_power (float or ndarray): Signal power in watts.
        noise_power (float): Noise power in watts.

    Returns:
        snr (float or ndarray): The signal-to-noise ratio (SNR) in decibels.
    """
    return 10 * np.log10(signal_power / noise_power)

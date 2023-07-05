"""
Compute system level metrics.
"""

import numpy as np


def get_outage(instantaneous_rate, target_rate):
    """
    Compute the outage probability.

    Args:
        instantaneous_rate: The instantaneous rate.
        target_rate: The target rate.

    Returns:
        The outage probability.
    """

    if isinstance(instantaneous_rate, list):
        outage = [1 if rate < target_rate else 0 for rate in instantaneous_rate]
    else:
        outage = 1 if instantaneous_rate < target_rate else 0

    return outage


def get_snr(signal_power, noise_power):
    """
    Calculate the signal-to-noise ratio (SNR) in decibels.

    Args:
        signal_power (float): Signal power in watts.
        noise_power (float): Noise power in watts.

    Returns:
        float: SNR in decibels.
    """
    return 10 * np.log10(signal_power / noise_power)

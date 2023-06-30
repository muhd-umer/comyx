"""
Compute outage metrics.
"""

import numpy as np


def outage_probability(instantaneous_rate, target_rate):
    """
    Compute the outage probability.

    Args:
        instantaneous_rate: The instantaneous rate.
        target_rate: The target rate.

    Returns:
        The outage probability.
    """

    if instantaneous_rate < target_rate:
        outage = 1
    else:
        outage = 0

    return outage

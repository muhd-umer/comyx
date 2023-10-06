from __future__ import annotations

from typing import Any, List, Union

import numpy as np
import numpy.typing as npt

NDArrayFloat = npt.NDArray[np.floating[Any]]
NDArraySigned = npt.NDArray[np.signedinteger[Any]]

def get_outage_instances(
    instantaneous_rate: Union[float, List[float]], target_rate: float
) -> Union[int, List[int]]:
    """Compute the instance(s) of outage.

    Args:
        instantaneous_rate: The instantaneous rate(s) of the link(s).
        target_rate: The target rate of the link.

    Returns:
        outage: The instance(s) of outage.
    """
    if isinstance(instantaneous_rate, list):
        outage = [1 if rate < target_rate else 0 for rate in instantaneous_rate]
    else:
        outage = 1 if instantaneous_rate < target_rate else 0

    return outage


def get_snr(
    signal_power: Union[float, NDArrayFloat], noise_power: float
<<<<<<< HEAD
) -> Union[float, NDArraySigned]:
=======
) -> Union[float, NDArrayInt]:
>>>>>>> 6b45b3e6cba439d167782934cac4654d7d0a19e1
    """Calculate the signal-to-noise ratio (SNR) in decibels.

    Args:
        signal_power: Signal power in watts.
        noise_power: Noise power in watts.

    Returns:
        snr: The signal-to-noise ratio (SNR) in decibels.
    """
    return 10 * np.log10(signal_power / noise_power)

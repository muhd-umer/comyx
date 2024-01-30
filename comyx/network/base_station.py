from __future__ import annotations

from typing import Any, List, Union

import numpy as np
import numpy.typing as npt

NDArrayFloat = npt.NDArray[np.floating[Any]]
RVDistribution = Any

from .transceiver import Transceiver


class BaseStation(Transceiver):
    """Represents a base station in the modelled environment.

    Identifiers may be of the form "BSx", where x is a positive integer. The
    first two characters indicate the type of transceiver, i.e., "BS" for base
    station. The remaining characters are the unique identifier of the base
    station. For example, "BS1" is a base station with identifier 1.
    """

    def __init__(
        self,
        id_: str,
        position: List[float],
        n_antennas: int,
        t_power: Union[float, None] = None,
        r_sensitivity: Union[float, None] = None,
    ):
        """Initialize a transceiver object.

        Args:
            id_: Unique identifier of the transceiver.
            position: Position of the transceiver in the environment.
            n_antennas: Number of antennas of the transceiver.
            t_power: Transmit power of the transceiver.
            r_sensitivity: Sensitivity of the transceiver.
        """
        super().__init__(id_, position, n_antennas, t_power, r_sensitivity)


__all__ = ["BaseStation"]

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
        n_antennas: int,
        position: Union[List[float], None] = None,
        t_power: Union[float, None] = None,
        r_sensitivity: Union[float, None] = None,
        radius: Union[float, None] = None,
    ):
        """Initialize a transceiver object.

        Args:
            id_: Unique identifier of the transceiver.
            n_antennas: Number of antennas of the transceiver.
            position: Position of the transceiver in the environment.
            t_power: Transmit power of the transceiver.
            r_sensitivity: Sensitivity of the transceiver.
            radius: Radius of the transceiver.
        """
        super().__init__(id_, n_antennas, position, t_power, r_sensitivity)

        self._radius = radius

    @property
    def radius(self) -> float:
        """Return the radius of the base station."""
        return self._radius


__all__ = ["BaseStation"]

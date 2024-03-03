from __future__ import annotations

from typing import Any, List, Union

import numpy as np
import numpy.typing as npt

NDArrayFloat = npt.NDArray[np.floating[Any]]
RVDistribution = Any


class Transceiver:
    """Represents a transceiver in the modelled environment.

    Fundamental class of Comyx environments; can be used to model both the base
    stations and the mobile stations/users.

    All transceivers have a unique identifier, a position in the environment, number
    of antennas, and optionally a transmit power and a sensitivity. The transmit power
    is the power at which a transceiver transmits signals, and the sensitivity is the
    minimum power at which a transceiver can receive signals.
    """

    def __init__(
        self,
        id_: str,
        n_antennas: int,
        position: Union[List[float], None] = None,
        t_power: Union[float, None] = None,
        r_sensitivity: Union[float, None] = None,
    ):
        """Initialize a transceiver object.

        Args:
            id_: Unique identifier of the transceiver.
            n_antennas: Number of antennas of the transceiver.
            position: Position of the transceiver in the environment.
            t_power: Transmit power of the transceiver.
            r_sensitivity: Sensitivity of the transceiver.
        """
        assert isinstance(id_, str), "ID must be a string."

        self._id = id_
        self._position = position
        self._n_antennas = n_antennas
        self._t_power = t_power
        self._r_sensitivity = r_sensitivity

    @property
    def id(self) -> str:
        """Return the unique identifier of the transceiver."""
        return self._id

    @property
    def position(self) -> List[float]:
        """Return the position of the transceiver in the environment."""
        return self._position

    @position.setter
    def position(self, new_position: List[float]) -> None:
        """Set the position of the transceiver in the environment."""
        self._position = new_position

    @property
    def n_antennas(self) -> int:
        """Return the number of antennas of the transceiver."""
        return self._n_antennas

    @property
    def t_power(self) -> Union[float, NDArrayFloat, None]:
        """Return the transmit power of the transceiver."""
        return self._t_power

    @property
    def r_sensitivity(self) -> Union[float, None]:
        """Return the sensitivity of the transceiver."""
        return self._r_sensitivity

    def __repr__(self) -> str:
        return f"{self.id}(position={self.position}, n_antennas={self.n_antennas})"


__all__ = ["Transceiver"]

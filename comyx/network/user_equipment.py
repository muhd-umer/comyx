from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Union

if TYPE_CHECKING:
    from .base_station import BaseStation

import random

import numpy as np
import numpy.typing as npt

NDArrayFloat = npt.NDArray[np.floating[Any]]
RVDistribution = Any

from .transceiver import Transceiver


class UserEquipment(Transceiver):
    """Represents a user equipment in the modelled environment.

    Identifiers may be of the form "UEx", where x is a positive integer. The
    first two characters indicate the type of transceiver, i.e., "UE" for user
    equipment. The remaining characters are the unique identifier of the user
    equipment. For example, "UE42" is a user equipment with identifier 42.
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
        super().__init__(id_, n_antennas, position, t_power, r_sensitivity)

    @property
    def rate(self, mean_axis=-1) -> NDArrayFloat:
        """Calculate the rate of the transceiver (Shannon formula)

        Args:
            mean_axis: Axis along which the mean is calculated.
              Default is -1 (last axis, i.e., over all realizations).

        Returns:
            Rate of the transceiver.
        """

        if not hasattr(self, "sinr"):
            raise ValueError("SINR not set")

        return np.mean(np.log2(1 + self.sinr), axis=mean_axis)

    @classmethod
    def from_base_station(
        cls,
        base_station: BaseStation,
        id_: str,
        n_antennas: int,
        t_power: Union[float, None] = None,
        r_sensitivity: Union[float, None] = None,
        height: float = 0,
        tolerance: float = 0,
    ) -> UserEquipment:
        """Create a user equipment within the coverage area of a base station.

        Args:
            id_: Unique identifier of the user equipment.
            n_antennas: Number of antennas of the user equipment.
            base_station: Base station to create the user equipment from.
            height: Height of the user equipment. Defaults to 0.
            tolerance: Tolerance from the edge of the coverage area.
              Defaults to 0.

        Returns:
            Randomly positioned user equipment.
        """

        assert base_station.radius is not None, "Base station radius must be set"
        assert base_station.position is not None, "Base station position must be set"

        angle = 2 * np.pi * random.random()
        r = (base_station.radius - tolerance) * np.sqrt(random.random())

        # Calculate the new x and y coordinates
        x = r * np.cos(angle) + base_station.position[0]
        y = r * np.sin(angle) + base_station.position[1]
        z = height

        position = [x, y, z]

        return cls(id_, n_antennas, position, t_power, r_sensitivity)


__all__ = ["UserEquipment"]

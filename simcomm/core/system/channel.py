from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ...utils import db2pow, get_distance
from ..fading import *
from ..propagation import *

if TYPE_CHECKING:
    from .receiver import Receiver
    from .transmitter import Transmitter


class Channel:
    """A class representing a wireless channel.

    Args:
        transmitter: The transmitter object.
        receiver: The receiver object.
        frequency: The frequency of the channel.
        fading_args: The arguments for the fading model.
        pathloss_args: The arguments for the pathloss model.
        size: The number of channel gains to generate.

    Attributes:
        transmitter: The transmitter object.
        receiver: The receiver object.
        frequency: The frequency of the channel.
        fading_args: The arguments for the fading model.
        pathloss_args: The arguments for the pathloss model.
        size: The number of channel gains to generate.
        distance: The distance between the transmitter and receiver.
        pathloss: The pathloss value.
        multipath_fading: The multipath fading values.

    Raises:
        ValueError: If the size is less than or equal to 0.

    Fading Args:
        type: The type of fading model to use.
        size: The number of channel gains to generate.
        ret: The return type, either "gains" or "coefficients".

        Rayleigh Fading Args:
            sigma: The scale factor of the Rayleigh distribution.

        Rician Fading Args:
            K: The K factor of the Rician distribution.
            sigma: The scale factor of the Rician distribution.

    Pathloss Args:
        type: The type of pathloss model to use.

        FSPL Args:
            alpha: The pathloss exponent.
            p0: The reference pathloss at 1m.

        Log Distance Args:
            alpha: The pathloss exponent.
            d0: The breakpoint distance.
            sigma: The standard deviation of the shadowing.
    """

    def __init__(
        self,
        transmitter: Transmitter,
        receiver: Receiver,
        frequency: float,
        fading_args: dict,
        pathloss_args: dict,
        size: int,
    ) -> None:
        self.transmitter = transmitter
        self.receiver = receiver
        self.frequency = frequency
        self.size = size
        self.distance = get_distance(self.transmitter.position, self.receiver.position)
        self.pathloss = get_pathloss(
            **pathloss_args, distance=self.distance, frequency=self.frequency
        )
        self.multipath_fading = get_multipath_fading(**fading_args, size=self.size)

    def generate_channel(self) -> np.ndarray:
        """Generates the channel coefficients from the multipath fading and pathloss values.

        Returns:
            The channel coefficients.
        """
        coefficients = np.sqrt(db2pow(-1 * self.pathloss)) * self.multipath_fading

        return coefficients
        return coefficients

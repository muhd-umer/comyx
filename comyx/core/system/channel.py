from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from ...utils import db2pow, get_distance
from ..fading import *
from ..propagation import *

if TYPE_CHECKING:
    from .system import SystemObject


class Channel:
    """A class representing a wireless channel. Used to generate channel coefficients. Also allows for the addition of external coefficients.

    Args:
        transmitter: The transmitter object.
        receiver: The receiver object.
        frequency: The frequency of the channel.
        fading_args: The arguments for the fading model.
        pathloss_args: The arguments for the pathloss model.
        shape: The number of channel gains to generate.
        no_link: If True, the complex fading is zero.

    Attributes:
        transmitter: Stores the transmitter object.
        receiver: Stores the receiver object.
        frequency: Stores the frequency of the channel.
        fading_args: Stores the arguments for the fading model.
        pathloss_args: Stores the arguments for the pathloss model.
        shape: Stores the shape of the channel coefficients.
        distance: Stores the distance between the transmitter and receiver.
        pathloss: Stores the pathloss between the transmitter and receiver.
        ext_coefficients: Stores the external coefficients of the channel.
        coefficients: Stores the channel coefficients.

    - Fading Args:
        - type: The type of fading model to use.
        - shape: The number of channel gains to generate.
        - ret: The return type, either "gains" or "coefficients".

        - Rayleigh Fading Args:
            - sigma: The scale factor of the Rayleigh distribution.

        - Rician Fading Args:
            - K: The K factor of the Rician distribution.
            - sigma: The scale factor of the Rician distribution.

    - Pathloss Args:
        - type: The type of pathloss model to use.

        - FSPL Args:
            - alpha: The pathloss exponent.
            - p0: The reference pathloss at 1m.

        - Log Distance Args:
            - alpha: The pathloss exponent.
            - d0: The breakpoint distance.
            - sigma: The standard deviation of the shadowing.
    """

    def __init__(
        self,
        transmitter: SystemObject,
        receiver: SystemObject,
        frequency: float,
        fading_args: dict[str, Any],
        pathloss_args: dict[str, Any],
        shape: tuple,
        no_link: bool = False,
    ) -> None:
        """Initializes the channel object.

        Args:
            transmitter: The transmitter object.
            receiver: The receiver object.
            frequency: The frequency of the channel.
            fading_args: The arguments for the fading model.
            pathloss_args: The arguments for the pathloss model.
            shape: The number of channel gains to generate.
            no_link: If True, the complex fading is zero.

        Fading Args:
            type: The type of fading model to use.
            shape: The number of channel gains to generate.
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
        self.transmitter = transmitter
        self.receiver = receiver
        self.frequency = frequency
        self.shape = shape
        self.fading_args = fading_args
        self.no_link = no_link
        self.distance = get_distance(
            self.transmitter.position, self.receiver.position, 3
        )
        self.pathloss = get_pathloss(
            **pathloss_args, distance=self.distance, frequency=self.frequency
        )
        self.generate_channel()

    def generate_channel(self) -> None:
        """Generates the channel coefficients from the multipath fading and pathloss values.

        Returns:
            None
        """
        if not self.no_link:
            dist_samples = get_rvs(**self.fading_args, shape=self.shape)
            phase = np.random.uniform(0, 2 * np.pi, self.shape)
            complex_fading = dist_samples * np.exp(1j * phase)
            self.coefficients = np.sqrt(db2pow(-1 * self.pathloss)) * complex_fading
        else:
            self.coefficients = np.zeros(self.shape, dtype=np.complex128)

    def update_channel(self, value) -> None:
        """Updates the channel coefficients from the multipath fading and pathloss values.

        Args:
            value: The value to add to the channel coefficients.

        Returns:
            None
        """
        self.coefficients += value

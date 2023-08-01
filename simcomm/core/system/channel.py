from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ...utils import db2pow, get_distance
from ..fading import *
from ..propagation import *

if TYPE_CHECKING:
    from .system import SystemObject


class Channel:
    """A class representing a wireless channel. Used to generate channel coefficients. Also allows for the addition of external coefficients.

    Args:
        transmitter (SystemObject): The transmitter object.
        receiver (SystemObject): The receiver object.
        frequency (float): The frequency of the channel.
        fading_args (dict): The arguments for the fading model.
        pathloss_args (dict): The arguments for the pathloss model.
        shape (tuple): The number of channel gains to generate.
        no_link (bool): If True, the complex fading is zero.


    Attributes:
        transmitter (SystemObject): Stores the transmitter object.
        receiver (SystemObject): Stores the receiver object.
        frequency (float): Stores the frequency of the channel.
        fading_args (dict): Stores the arguments for the fading model.
        pathloss_args (dict): Stores the arguments for the pathloss model.
        shape (tuple): Stores the shape of the channel coefficients.
        distance (float): Stores the distance between the transmitter and receiver.
        pathloss (float): Stores the pathloss between the transmitter and receiver.
        ext_coefficients (array_like): Stores the external coefficients of the channel.
        coefficients (array_like): Stores the channel coefficients.

    - Fading Args:
        - type (str): The type of fading model to use.
        - shape (int): The number of channel gains to generate.
        - ret (str): The return type, either "gains" or "coefficients".

        - Rayleigh Fading Args:
            - sigma (float): The scale factor of the Rayleigh distribution.

        - Rician Fading Args:
            - K (float): The K factor of the Rician distribution.
            - sigma (float): The scale factor of the Rician distribution.

    - Pathloss Args:
        - type (str): The type of pathloss model to use.

        - FSPL Args:
            - alpha (float): The pathloss exponent.
            - p0 (float): The reference pathloss at 1m.

        - Log Distance Args:
            - alpha (float): The pathloss exponent.
            - d0 (float): The breakpoint distance.
            - sigma (float): The standard deviation of the shadowing.
    """

    def __init__(
        self,
        transmitter: SystemObject,
        receiver: SystemObject,
        frequency: float,
        fading_args: dict,
        pathloss_args: dict,
        shape: tuple,
        no_link: bool = False,
    ) -> None:
        """Initializes the channel object.

        Args:
        transmitter (SystemObject): The transmitter object.
        receiver (Receiver): The receiver object.
        frequency (float): The frequency of the channel.
        fading_args (dict): The arguments for the fading model.
        pathloss_args (dict): The arguments for the pathloss model.
        shape (tuple): The number of channel gains to generate.
        no_link (bool): If True, the complex fading is zero.

        Fading Args:
            type (str): The type of fading model to use.
            shape (int): The number of channel gains to generate.
            ret (str): The return type, either "gains" or "coefficients".

            Rayleigh Fading Args:
                sigma (float): The scale factor of the Rayleigh distribution.

            Rician Fading Args:
                K (float): The K factor of the Rician distribution.
                sigma (float): The scale factor of the Rician distribution.

        Pathloss Args:
            type (str): The type of pathloss model to use.

            FSPL Args:
                alpha (float): The pathloss exponent.
                p0 (float): The reference pathloss at 1m.

            Log Distance Args:
                alpha (float): The pathloss exponent.
                d0 (float): The breakpoint distance.
                sigma (float): The standard deviation of the shadowing.
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
        """
        Generates the channel coefficients from the multipath fading and pathloss values.

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
        """
        Updates the channel coefficients from the multipath fading and pathloss values.

        Args:
            value (array_like): The value to add to the channel coefficients.

        Returns:
            None
        """
        self.coefficients += value


__all__ = ["Channel"]

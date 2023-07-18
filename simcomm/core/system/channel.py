"""
Implements the channel class.
"""

import numpy as np

from ...utils import db2pow, get_distance
from ..fading import *
from ..propagation import *
from . import Reciever, Transmitter


class Channel:
    """
    A class representing a wireless channel.

    Attributes:
        transmitter (Transmitter): The transmitter object.
        receiver (Receiver): The receiver object.
        frequency (float): The frequency of the channel.
        fading_args (dict): The arguments for the fading model.
        pathloss_args (dict): The arguments for the pathloss model.
        size (int): The number of channel gains to generate.

    Fading Args:
        type (str): The type of fading model to use.
        size (int): The number of channel gains to generate.
        library (str): The library to use for the fading model.

        Rayleigh Fading Args:
            sigma (float): The scale factor of the Rayleigh distribution.

        Rician Fading Args:
            K (float): The K factor of the Rician distribution.
            sigma (float): The scale factor of the Rician distribution.

    Pathloss Args:
        type (str): The type of pathloss model to use.

        Simple Args:
            alpha (float): The pathloss exponent.

        Log Distance Args:
            alpha (float): The pathloss exponent.
            d_break (float): The breakpoint distance.
            sigma (float): The standard deviation of the shadowing.
    """

    def __init__(
        self,
        transmitter: Transmitter,
        receiver: Reciever,
        frequency,
        fading_args,
        pathloss_args,
        size,
    ):
        self.transmitter = transmitter
        self.receiver = receiver
        self.frequency = frequency
        self.pathloss_args = get_pathloss(
            **pathloss_args, distance=self.distance, frequency=self.frequency
        )
        self.multipath_fading = get_multipath_fading(**fading_args)
        self.size = size
        self.distance = get_distance(self.transmitter.position, self.receiver.position)

    def generate_channel(self):
        """
        Generates the channel gains from the multipath fading and pathloss values.

        Returns:
            Channel gains in linear scale.
        """
        channel_gains = np.sqrt(db2pow(-1 * self.pathloss)) * self.multipath_fading

        return channel_gains

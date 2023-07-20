from typing import Union

from .channel import *
from .receiver import *
from .star import *
from .system import *
from .transmitter import *


class LinkCollection:
    """
    Contains a collection of links accessible by name.

    Attributes:
        links (dict): A dictionary of links.
        link_types (dict): A dictionary of link types.
        size (int): The size of the links.
    """

    def __init__(self, size: int):
        """
        Initializes a new instance of the LinkCollection class.

        Args:
            size (int): The size of the links.
        """
        self.links = {}
        self.link_types = {}
        self.size = size

    def add_link(
        self,
        transmitter: Union[Transmitter, STAR],
        receiver: Receiver,
        channel: Channel,
        type: str,
    ) -> None:
        """
        Adds a link to the collection.

        Args:
            transmitter (Transmitter or STAR): The transmitter object.
            receiver (Receiver): The receiver object.
            channel (Channel): The channel object.
            type (str): The type of link. ("1C", "2C") for center users, "E" for edge users, "RIS" for RIS.
        """
        assert type in ["1C", "2C", "E", "RIS"], "Invalid link type."
        self.links[transmitter.name, receiver.name] = channel.generate_channel()
        self.link_types[transmitter.name, receiver.name] = type

    def get_link(
        self, transmitter: Union[Transmitter, STAR], receiver: Receiver
    ) -> np.ndarray:
        """
        Gets the channel between a transmitter and receiver.

        Args:
            transmitter (Transmitter or STAR): The transmitter object.
            receiver (Receiver): The receiver object.

        Returns:
            The channel between the transmitter and receiver.
        """
        return self.links[transmitter.name, receiver.name]

    def get_link_type(
        self, transmitter: Union[Transmitter, STAR], receiver: Receiver
    ) -> str:
        """
        Gets the type of link between a transmitter and receiver.

        Args:
            transmitter (Transmitter or STAR): The transmitter object.
            receiver (Receiver): The receiver object.

        Returns:
            The type of link between the transmitter and receiver.
        """
        return self.link_types[transmitter.name, receiver.name]

    def update_link(
        self,
        transmitter: Union[Transmitter, STAR],
        receiver: Receiver,
        value: np.ndarray,
    ) -> None:
        """
        Combines a value with the channel between a transmitter and receiver.

        Args:
            transmitter (Transmitter or STAR): The transmitter object.
            receiver (Receiver): The receiver object.
            value (ndarray): The value to combine with the channel.

        Returns:
            The combined channel between the transmitter and receiver.
        """
        assert value.shape == self.links[transmitter.name, receiver.name].shape
        self.links[transmitter.name, receiver.name] = (
            self.links[transmitter.name, receiver.name] + value
        )

    def __str__(self):
        """
        Returns a string representation of the LinkCollection.

        Returns:
            A string representation of the LinkCollection.
        """
        return "\n".join([f"{k[0]} -> {k[1]}" for k in self.links.keys()])

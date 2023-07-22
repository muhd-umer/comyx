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
        frequency (float): The frequency of the carrier signal in Hz.
    """

    def __init__(
        self,
        size: int,
        frequency: float,
    ):
        """
        Initializes a new instance of the LinkCollection class.

        Args:
            size (int): The size of the links.
            frequency (float): The frequency of the carrier signal in Hz.
        """
        self.links = {}
        self.link_types = {}
        self.size = size
        self.frequency = frequency

    def add_link(
        self,
        transmitter: Union[Transmitter, STAR],
        receiver: Receiver,
        fading_args: dict,
        pathloss_args: dict,
        type: str,
        elements: int = None,
    ) -> None:
        """
        Adds a link to the collection.

        Args:
            transmitter (Transmitter or STAR): The transmitter object.
            receiver (Receiver): The receiver object.
            fading_args (dict): The arguments for the fading model.
            pathloss_args (dict): The arguments for the pathloss model.
            type (str): The type of link. Can be "1C", "2C", "E", "RIS", or "DNE".
            elements (int): The number of elements in the link.
        """
        assert type in ["1C", "2C", "E", "RIS", "DNE"], "Invalid link type."

        no_link = False
        if type == "RIS":
            assert (
                elements is not None
            ), "Number of elements must be specified for RIS links."
            link_size = (elements, self.size, 1)
        elif type == "DNE":
            no_link = True
            link_size = (self.size, 1)
        else:
            link_size = (self.size, 1)

        self.links[transmitter.name, receiver.name] = Channel(
            transmitter,
            receiver,
            self.frequency,
            fading_args,
            pathloss_args,
            link_size,
            no_link,
        )
        self.link_types[transmitter.name, receiver.name] = type

    def get_link(
        self,
        transmitter: Union[Transmitter, STAR],
        receiver: Receiver,
    ) -> np.ndarray:
        """
        Gets the channel between a transmitter and receiver.

        Args:
            transmitter (Transmitter or STAR): The transmitter object.
            receiver (Receiver): The receiver object.

        Returns:
            The channel between the transmitter and receiver.
        """

        return self.links[transmitter.name, receiver.name].coefficients

    def get_gain(self, transmitter: Transmitter, receiver: Receiver) -> float:
        """
        Gets the gain between a transmitter and receiver.

        Args:
            transmitter (Transmitter): The transmitter object.
            receiver (Receiver): The receiver object.

        Returns:
            The gain between the transmitter and receiver.
        """
        return np.abs(self.links[transmitter.name, receiver.name].coefficients) ** 2

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
        assert (
            value.shape
            == self.links[transmitter.name, receiver.name].coefficients.shape
        ), "Value to combine must have the same shape as the channel."

        phase = wrapTo2Pi(np.angle(self.get_link(transmitter, receiver)))
        self.links[transmitter.name, receiver.name].update_channel(
            value * np.exp(1j * phase)
        )

    def __str__(self):
        """
        Returns a string representation of the LinkCollection.

        Returns:
            A string representation of the LinkCollection. Displays links as "Transmitter -> Receiver" along with the type of link and shape of the channel.
        """
        string = ""
        for link in self.links:
            string += (
                f"{link[0]} -> {link[1]} | Type: ({self.link_types[link]}) | Shape: "
                f"{self.links[link].coefficients.shape}\n"
            )

        return string

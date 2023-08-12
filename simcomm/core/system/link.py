from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np
import numpy.typing as npt

from ...utils import wrapTo2Pi
from .channel import Channel

if TYPE_CHECKING:
    from .system import SystemObject


class LinkCollection:
    """Contains a collection of links accessible by name. Used to store all the channel coefficients and their corresponding types for the system under test.

    Args:
        size: The size of the links.
        frequency: The frequency of the carrier signal in Hz.
        link_config: The configuration for the links.

    Attributes:
        links: A dictionary of links.
        link_types: A dictionary of link types.
        size: The size of the links.
        frequency: The frequency of the carrier signal in Hz.
    """

    def __init__(
        self,
        size: int,
        frequency: float,
    ):
        """Initializes a new instance of the LinkCollection class.

        Args:
            size: The size of the links.
            frequency: The frequency of the carrier signal in Hz.
        """
        self.links = {}
        self.link_types = {}
        self.size = size
        self.frequency = frequency

    def add_link(
        self,
        transmitter: SystemObject,
        receiver: SystemObject,
        fading_args: dict,
        pathloss_args: dict,
        type: str,
    ) -> None:
        """Adds a link to the collection.

        Args:
            transmitter: The transmitter object.
            receiver: The receiver object.
            fading_args: The arguments for the fading model.
            pathloss_args: The arguments for the pathloss model.
            type: The type of link. Can be "1,c", "2,c", "f", "ris,f", "ris,atb1", "ris,atb2", or "dne".
        """
        assert type in [
            "1,c",
            "2,c",
            "f",
            "ris,f",
            "ris,b1",
            "ris,b2",
            "i,c",
            "dne",
        ], "Invalid link type."

        no_link = False
        if type == "ris,f":
            assert hasattr(
                transmitter, "elements"
            ), "Transmitter must have an 'elements' attribute for RIS links."
            link_size = (transmitter.elements, self.size, 1)  # type: ignore
        elif type == "ris,atb1":
            assert hasattr(
                transmitter, "assignments"
            ), "Transmitter must have an 'assignments' attribute for RIS links."
            link_size = (transmitter.assignments["BS1"], self.size, 1)  # type: ignore
        elif type == "ris,atb2":
            assert hasattr(
                transmitter, "assignments"
            ), "Transmitter must have an 'elements' attribute for RIS links."
            link_size = (transmitter.assignments["BS2"], self.size, 1)  # type: ignore
        elif type == "dne":
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
        transmitter: SystemObject,
        receiver: SystemObject,
    ) -> npt.NDArray[np.complexfloating[Any, Any]]:
        """Gets the channel between a transmitter and receiver.

        Args:
            transmitter: The transmitter object.
            receiver: The receiver object.

        Returns:
            The channel between the transmitter and receiver.
        """

        return self.links[transmitter.name, receiver.name].coefficients

    def get_gain(
        self, transmitter: SystemObject, receiver: SystemObject
    ) -> npt.NDArray[np.floating[Any]]:
        """Gets the gain between a transmitter and receiver.

        Args:
            transmitter: The transmitter object.
            receiver: The receiver object.

        Returns:
            The gain between the transmitter and receiver.
        """
        return np.abs(self.links[transmitter.name, receiver.name].coefficients) ** 2

    def get_link_type(self, transmitter: SystemObject, receiver: SystemObject) -> str:
        """Gets the type of link between a transmitter and receiver.

        Args:
            transmitter: The transmitter object.
            receiver: The receiver object.

        Returns:
            The type of link between the transmitter and receiver.
        """
        return self.link_types[transmitter.name, receiver.name]

    def update_link(
        self,
        transmitter: SystemObject,
        receiver: SystemObject,
        value: npt.NDArray[np.floating[Any]],
    ) -> None:
        """Combines a value with the channel between a transmitter and receiver.

        Args:
            transmitter: The transmitter object.
            receiver: The receiver object.
            value: The value to combine with the channel.

        Returns:
            None
        """
        assert (
            value.shape
            == self.links[transmitter.name, receiver.name].coefficients.shape
        ), "Value to combine must have the same shape as the channel."

        phase = wrapTo2Pi(np.angle(self.get_link(transmitter, receiver)))
        self.links[transmitter.name, receiver.name].update_channel(
            value * np.exp(1j * phase)
        )

    def __str__(self) -> str:
        """Returns a string representation of the LinkCollection.

        Returns:
            A string representation of the LinkCollection. Displays links as "Transmitter
            -> Receiver" along with the type of link and shape of the channel.
        """
        string = ""
        for link in self.links:
            string += (
                f"{link[0]} -> {link[1]} | Type: ({self.link_types[link]}) | Shape: "
                f"{self.links[link].coefficients.shape}\n"
            )

        return string

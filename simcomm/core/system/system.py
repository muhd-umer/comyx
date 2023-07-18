"""
Implementation of integral system objects.
"""

import numpy as np

from . import Channel, Receiver, Transmitter


class SystemObject:
    """
    Base class for all system objects.

    Attributes:
        name: The name of the system object.
        position: [x, y] coordinates of the system object.
                  [x, y, z] coordinates if 3D.
        antenna_gain: G, the gain of the antenna.
        losses: Lf, the losses of the system object.
    """

    def __init__(self, name, position, antenna_gain, losses):
        self.name = name
        self.position = position
        self.antenna_gain = antenna_gain
        self.losses = losses

    def __str__(self):
        return f"{self.name} at {self.position}"


class LinkCollection:
    """
    Contains a collection of links accessible by name.

    Attributes:
        links (dict): A dictionary of links.
    """

    def __init__(self):
        self.links = {}

    def add_link(self, transmitter: Transmitter, receiver: Receiver, channel: Channel):
        """
        Adds a link to the collection.

        Args:
            transmitter (Transmitter): The transmitter object.
            receiver (Receiver): The receiver object.
            channel (Channel): The channel object.
        """
        self.links[transmitter.name, receiver.name] = channel.generate_channel()

    def get_link(self, transmitter: Transmitter, receiver: Receiver):
        """
        Gets the channel between a transmitter and receiver.

        Args:
            transmitter (Transmitter): The transmitter object.
            receiver (Receiver): The receiver object.

        Returns:
            The channel between the transmitter and receiver.
        """
        return self.links[transmitter.name, receiver.name]

    def __str__(self):
        return "\n".join([f"{k[0]} -> {k[1]}" for k in self.links.keys()])


class Simulation:
    """
    Contains a collection of system objects and links.

    Attributes:
        system_objects (dict): A dictionary of system objects.
        links (LinkCollection): A collection of links.
    """

    def __init__(self):
        self.system_objects = {}
        self.links = LinkCollection()

    def add_system_object(self, system_object: SystemObject):
        """
        Adds a system object to the simulation.

        Args:
            system_object (SystemObject): The system object to add.
        """
        self.system_objects[system_object.name] = system_object

    def get_system_object(self, name: str):
        """
        Gets a system object from the simulation.

        Args:
            name (str): The name of the system object to get.

        Returns:
            The system object with the given name.
        """
        return self.system_objects[name]

    def __str__(self):
        return "\n".join([str(v) for v in self.system_objects.values()])

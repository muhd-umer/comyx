from __future__ import annotations

from typing import TYPE_CHECKING, List

import numpy as np

from .system import SystemObject

if TYPE_CHECKING:
    from . import LinkCollection
    from .receiver import Receiver
    from .transmitter import Transmitter


class STAR(SystemObject):
    """A class representing a STAR-RIS.

    Inherits from SystemObject. Passive in nature, can only reflect the incoming signal.

    Attributes:
        elements (int): The number of elements in the RIS.
        beta_r (float): The reflection coefficient of the RIS.
        theta_r (float): The reflection angle of the RIS.
        beta_t (float): The transmission coefficient of the RIS.
        theta_t (float): The transmission angle of the RIS.
        transmission_matrix (np.ndarray): The transmission matrix of the RIS.
        reflection_matrix (np.ndarray): The reflection matrix of the RIS.

    Inherited Attributes:
        name (str): The name of the system object.
        position (List[float]): [x, y] coordinates of the system object.
                                [x, y, z] coordinates if 3D.

    Args:
        name (str): The name of the STAR-RIS.
        position (List[float]): [x, y] coordinates of the STAR-RIS.
                                [x, y, z] coordinates if 3D.
        elements (int): The number of elements in the RIS.

    Raises:
        AssertionError: If the number of elements is not even.

    """

    def __init__(self, name: str, position: List[float], elements: int) -> None:
        super().__init__(name, position, None, None)
        assert elements % 2 == 0, "The number of elements must be even."
        self.elements = elements
        self.elements_per_bs = self.elements // 2
        self.beta_r = None
        self.theta_r = None
        self.beta_t = None
        self.theta_t = None
        self.transmission_matrix = None
        self.reflection_matrix = None

    def set_reflection_parameters(
        self,
        links: LinkCollection,
        transmitters: List[Transmitter],
        receivers: List[Receiver],
    ) -> None:
        """Sets the reflection parameters of the RIS.

        Args:
            links (LinkCollection): The collection of links in the system.
            transmitters (List[Transmitter]): The list of transmitters in the system.
            receivers (List[Receiver]): The list of receivers in the system.

        Raises:
            AssertionError: If there are not exactly 2 base stations or 2 cell-center receivers.
        """
        assert len(transmitters) == 2, "There must be exactly 2 base stations."
        assert len(receivers) == 2, "There must be exactly 2 cell-center receivers."

        bs1_u1c, bs2_u2c = (
            links.get_link(transmitters[0], receivers[0]),
            links.get_link(transmitters[1], receivers[1]),
        )

        bs1_ris, bs2_ris = (
            links.get_link(transmitters[0], self),
            links.get_link(transmitters[1], self),
        )
        ris_u1c, ris_u2c = (
            links.get_link(self, receivers[0]),
            links.get_link(self, receivers[1]),
        )

        self.theta_r = np.zeros((self.elements, links.size, 1))

        for i in range(self.elements_per_bs):
            self.theta_r[i] = np.angle(bs1_u1c) - np.angle(bs1_ris * ris_u1c)
            self.theta_r[i + self.elements_per_bs] = np.angle(bs2_u2c) - np.angle(
                bs2_ris * ris_u2c
            )

        self.beta_r = np.ones((self.elements, links.size, 1)) * 0.5

        self.reflection_matrix = np.zeros(
            (self.elements, self.elements, links.size, 1), dtype=np.complex128
        )

        for i in range(self.elements):
            self.reflection_matrix[i, i] = self.beta_r[i] * np.exp(1j * self.theta_r[i])

    def set_transmission_parameters(
        self,
        links: LinkCollection,
        transmitters: List[Transmitter],
        receiver: Receiver,
    ) -> None:
        """Sets the transmission parameters of the RIS.

        Args:
            links (LinkCollection): The collection of links in the system.
            transmitters (List[Transmitter]): The list of transmitters in the system.
            receiver (Receiver): The far receiver (UF) in the system.

        Raises:
            AssertionError: If there are not exactly 2 base stations.
        """
        assert len(transmitters) == 2, "There must be exactly 2 base stations."

        bs1_uf, bs2_uf = links.get_link(transmitters[0], receiver), links.get_link(
            transmitters[1], receiver
        )
        bs1_ris, bs2_ris = links.get_link(transmitters[0], receiver), links.get_link(
            transmitters[1], self
        )
        ris_uf = links.get_link(self, receiver)[1]

        self.theta_t = np.zeros((self.elements, links.size, 1))

        self.theta_t[: self.elements_per_bs] = np.angle(bs1_uf) - np.angle(
            bs1_ris * ris_uf
        )
        self.theta_t[self.elements_per_bs :] = np.angle(bs2_uf) - np.angle(
            bs2_ris * ris_uf
        )

        self.beta_t = np.ones((self.elements, links.size, 1)) * 0.5

        self.transmission_matrix = np.zeros(
            (self.elements, self.elements, links.size, 1), dtype=np.complex128
        )

        for i in range(self.elements):
            self.transmission_matrix[i, i] = self.beta_t[i] * np.exp(
                1j * self.theta_t[i]
            )

    def update_link(
        self,
        links: LinkCollection,
        transmitter: Transmitter,
        receiver: Receiver,
    ) -> None:
        """Updates the link between the Transmitter and Receiver with combined channel.
        Expects the arguments to be in the order as link is defined.

        Args:
            links (LinkCollection): The collection of links in the system.
            transmitters (Transmitter): The transmitter in the system.
            receiver (Receiver): The receiver in the system.

        Raises:
            AssertionError: If there are not exactly 2 base stations or 3 receivers.
        """
        ris_addition = np.zeros((links.size, 1), dtype=np.complex128)

        if links.get_link_type(transmitter, receiver) == "E":
            for i in range(self.elements):
                ris_addition += (
                    np.conj(links.get_link(self, receiver)[i])
                    * np.sqrt(self.beta_t[i])
                    * np.exp(1j * self.theta_t[i])
                    * links.get_link(transmitter, self)[i]
                )
            links.update_link(transmitter, receiver, ris_addition)

        elif links.get_link_type(transmitter, receiver) == "1C":
            for i in range(self.elements_per_bs):
                ris_addition += (
                    np.conj(links.get_link(self, receiver)[i])
                    * np.sqrt(self.beta_r[i])
                    * np.exp(1j * self.theta_r[i])
                    * links.get_link(transmitter, self)[i]
                )

        elif links.get_link_type(transmitter, receiver) == "2C":
            for i in range(self.elements_per_bs):
                ris_addition += (
                    np.conj(links.get_link(self, receiver)[i])
                    * np.sqrt(self.beta_r[i + self.elements_per_bs])
                    * np.exp(1j * self.theta_r[i + self.elements_per_bs])
                    * links.get_link(transmitter, self)[i]
                )

        else:
            raise NotImplementedError("Invalid link type.")

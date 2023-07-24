from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

import numpy as np

from ...utils import wrapTo2Pi
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
        beta_r (np.ndarray): The reflection coefficients of the RIS.
        theta_r (np.ndarray): The phase shifts of the RIS.
        beta_t (np.ndarray): The transmission coefficients of the RIS.
        theta_t (np.ndarray): The phase shifts of the RIS.
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

    def __init__(
        self,
        name: str,
        position: List[float],
        elements: int,
        beta_r: float = 0.5,
        beta_t: float = 0.5,
        custom_assignment: dict = None,
    ) -> None:
        """Initializes the STAR-RIS object.

        Args:
            name (str): The name of the STAR-RIS.
            position (List[float]): [x, y] coordinates of the STAR-RIS.
                                    [x, y, z] coordinates if 3D.
            elements (int): The number of elements in the RIS.
            beta_r (float, optional): The reflection coefficients of the RIS. Defaults to 0.5.
            beta_t (float, optional): The transmission coefficients of the RIS. Defaults to 0.5.

        """
        super().__init__(name, position)
        if custom_assignment is None:
            assert elements % 2 == 0, "The number of elements must be even."
            self.elements = elements
            self.elements_per_bs1 = elements // 2
            self.elements_per_bs2 = self.elements - self.elements_per_bs1
        else:
            assert isinstance(
                custom_assignment, dict
            ), "custom_assignment must be a dictionary."
            self.elements = elements
            self.elements_per_bs1 = custom_assignment["bs1"]
            self.elements_per_bs2 = custom_assignment["bs2"]

        assert beta_r + beta_t == 1, "beta_r + beta_t must be equal to 1."

        self.beta_r = np.ones((self.elements, 1, 1)) * beta_r
        self.beta_t = np.ones((self.elements, 1, 1)) * beta_t

        self.theta_r = None
        self.theta_t = None

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

        self.theta_r[: self.elements_per_bs1] = wrapTo2Pi(
            wrapTo2Pi(np.angle(bs1_u1c))
            - (wrapTo2Pi(np.angle(bs1_ris)) + wrapTo2Pi(np.angle(ris_u1c)))
        )
        self.theta_r[self.elements_per_bs1 :] = wrapTo2Pi(
            wrapTo2Pi(np.angle(bs2_u2c))
            - (wrapTo2Pi(np.angle(bs2_ris)) + wrapTo2Pi(np.angle(ris_u2c)))
        )

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
        ris_uf = links.get_link(self, receiver)

        self.theta_t = np.zeros((self.elements, links.size, 1))

        self.theta_t[: self.elements_per_bs1] = wrapTo2Pi(
            wrapTo2Pi(np.angle(bs1_uf))
            - (
                wrapTo2Pi(np.angle(bs1_ris))
                + wrapTo2Pi(np.angle(ris_uf[: self.elements_per_bs1]))
            )
        )
        self.theta_t[self.elements_per_bs1 :] = wrapTo2Pi(
            wrapTo2Pi(np.angle(bs2_uf))
            - (
                wrapTo2Pi(np.angle(bs2_ris))
                + wrapTo2Pi(np.angle(ris_uf[self.elements_per_bs1 :]))
            )
        )

    def merge_link(
        self,
        links: LinkCollection,
        transmitter: Union[Transmitter, List[Transmitter]],
        receiver: Receiver,
    ) -> None:
        """Updates the link between the Transmitter and Receiver with combined channel.
        Expects the arguments to be in the order as link is defined.

        Args:
            links (LinkCollection): The collection of links in the system.
            transmitters (Union[Transmitter, List[Transmitter]]): The transmitter(s) in the system. Pass a list of transmitters if link type between Transmitter and Receiver is "E".
            receiver (Receiver): The receiver in the system.

        Raises:
            AssertionError: If there are not exactly 2 base stations or 3 receivers.
        """
        if isinstance(transmitter, list):
            assert (
                links.get_link_type(transmitter[0], receiver) == "E"
                or links.get_link_type(transmitter[0], receiver) == "DNE"
            ) and (
                links.get_link_type(transmitter[1], receiver) == "E"
                or links.get_link_type(transmitter[1], receiver) == "DNE"
            ), "Both BS1 -> UF and BS2 -> UF must be 'E' or 'DNE' links."

            ris_1h_val = np.zeros((links.size, 1), dtype=np.float64)
            ris_2h_val = np.zeros((links.size, 1), dtype=np.float64)

            for i in range(self.elements_per_bs1):
                ris_1h_val += np.abs(
                    np.conj(links.get_link(self, receiver)[i])
                    * np.sqrt(self.beta_t[i])
                    * np.exp(1j * self.theta_t[i])
                    * links.get_link(transmitter[0], self)[i]
                )
            for k in range(self.elements_per_bs2):
                ris_2h_val += np.abs(
                    np.conj(links.get_link(self, receiver)[k + self.elements_per_bs1])
                    * np.sqrt(self.beta_t[k + self.elements_per_bs1])
                    * np.exp(1j * self.theta_t[k + self.elements_per_bs1])
                    * links.get_link(transmitter[1], self)[k]
                )

            links.update_link(transmitter[0], receiver, ris_1h_val)
            links.update_link(transmitter[1], receiver, ris_2h_val)

        elif links.get_link_type(transmitter, receiver) == "1C":
            ris_addition = np.zeros((links.size, 1), dtype=np.float64)

            for i in range(self.elements_per_bs1):
                ris_addition += np.abs(
                    np.conj(links.get_link(self, receiver)[i])
                    * np.sqrt(self.beta_r[i])
                    * np.exp(1j * self.theta_r[i])
                    * links.get_link(transmitter, self)[i]
                )

            links.update_link(transmitter, receiver, ris_addition)

        elif links.get_link_type(transmitter, receiver) == "2C":
            ris_addition = np.zeros((links.size, 1), dtype=np.float64)

            for i in range(self.elements_per_bs2):
                ris_addition += np.abs(
                    np.conj(links.get_link(self, receiver)[i])
                    * np.sqrt(self.beta_r[i + self.elements_per_bs2])
                    * np.exp(1j * self.theta_r[i + self.elements_per_bs2])
                    * links.get_link(transmitter, self)[i]
                )

            links.update_link(transmitter, receiver, ris_addition)

        else:
            raise NotImplementedError("Invalid link type.")

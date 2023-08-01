from __future__ import annotations

from typing import List, Union

import numpy as np

from ...utils import wrapTo2Pi
from . import link as link
from .system import SystemObject


class STAR(SystemObject):
    """A class representing a STAR-RIS. Inherits from SystemObject. Passive in nature, can only reflect the incoming signal.

    Args:
        name (str): The name of the STAR-RIS.
        position (List[float]): [x, y] coordinates of the STAR-RIS, [x, y, z] coordinates if 3D.
        elements (int): The number of elements in the RIS.
        beta_r (float, optional): The reflection coefficients of the RIS. Defaults to 0.5.
        beta_t (float, optional): The transmission coefficients of the RIS. Defaults to 0.5.
        custom_assignment (dict): Custom  assignment, i.e., different number of elements assigned to BS1 and BS2 or beta_r and beta_t other than halved.

    Attributes:
        name (str): Stores the name of the system object.
        position (List[float]): Stores the [x, y] coordinates of the system object, [x, y, z] coordinates if 3D.
        elements (int): Stores the number of elements in the RIS.
        beta_r (ndarray): Stores the reflection coefficients of the RIS.
        theta_r (ndarray): Stores the phase shifts of the RIS.
        beta_t (ndarray): Stores the transmission coefficients of the RIS.
        theta_t (ndarray): Stores the phase shifts of the RIS.
        custom_assignment (dict): Stores the custom assignment, i.e., different number of elements assigned to BS1 and BS2 or beta_r and beta_t other than halved.
        transmission_matrix (ndarray): Stores the transmission matrix of the RIS.
        reflection_matrix (ndarray): Stores the reflection matrix of the RIS.
    """

    def __init__(
        self,
        name: str,
        position: List[float],
        elements: int,
        beta_r: float = 0.5,
        beta_t: float = 0.5,
        custom_assignment: Union[dict, None] = None,
    ) -> None:
        """Initializes the STAR-RIS object.

        Args:
            name (str): The name of the STAR-RIS.
            position (List[float]): [x, y] coordinates of the STAR-RIS, [x, y, z] coordinates if 3D.
            elements (int): The number of elements in the RIS.
            beta_r (float, optional): The reflection coefficients of the RIS. Defaults to 0.5.
            beta_t (float, optional): The transmission coefficients of the RIS. Defaults to 0.5.
            custom_assignment (dict): Custom  assignment, i.e., different number of elements assigned to BS1 and BS2 or beta_r and beta_t other than halved.
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
            assert self.elements_per_bs1 + self.elements_per_bs2 == self.elements, (
                "The number of elements in the RIS must be equal to the sum of"
                "the number of elements assigned to BS1 and BS2."
            )

        assert beta_r + beta_t == 1, "beta_r + beta_t must be equal to 1."

        self.beta_r = np.ones((self.elements, 1, 1)) * beta_r
        self.beta_t = np.ones((self.elements, 1, 1)) * beta_t

    def set_reflection_parameters(
        self,
        links: link.LinkCollection,
        transmitters: List[SystemObject],
        receivers: List[SystemObject],
    ) -> None:
        """Sets the reflection parameters of the RIS.

        Args:
            links (link.LinkCollection): The collection of links in the system.
            transmitters (List[SystemObject]): The list of transmitters in the system.
            receivers (List[SystemObject]): The list of receivers in the system.

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
        links: link.LinkCollection,
        transmitters: List[SystemObject],
        receiver: SystemObject,
    ) -> None:
        """Sets the transmission parameters of the RIS.

        Args:
            links (link.LinkCollection): The collection of links in the system.
            transmitters (List[SystemObject]): The list of transmitters in the system.
            receiver (SystemObject): The far receiver (UF) in the system.

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
        links: link.LinkCollection,
        transmitter: Union[SystemObject, List[SystemObject]],
        receiver: SystemObject,
    ) -> None:
        """Updates the link between the SystemObject and SystemObject with combined channel. Expects the arguments to be in the order as link is defined.

        Args:
            links (link.LinkCollection): The collection of links in the system.
            transmitter (Union[SystemObject, List[SystemObject]]): The transmitter(s) in the system. Pass a list of transmitters if link type between SystemObject and SystemObject is "E".
            receiver (SystemObject): The receiver in the system.

        Raises:
            AssertionError: If there are not exactly 2 base stations or 3 receivers.
        """
        assert (
            self.theta_r is not None and self.theta_t is not None
        ), "The reflection and transmission parameters must be set before merging"

        if isinstance(transmitter, list):
            assert (
                links.get_link_type(transmitter[0], receiver) == "f"
                or links.get_link_type(transmitter[0], receiver) == "dne"
            ) and (
                links.get_link_type(transmitter[1], receiver) == "f"
                or links.get_link_type(transmitter[1], receiver) == "dne"
            ), "Both BS1 -> Uf and BS2 -> Uf must be 'f' or 'dne' links."

            ris_1h_val = np.zeros((links.size, 1), dtype=np.float64)
            ris_2h_val = np.zeros((links.size, 1), dtype=np.float64)

            for i in range(self.elements_per_bs1):
                ris_1h_val += np.abs(
                    np.conj(links.get_link(self, receiver)[i])
                    * np.sqrt(self.beta_t[i])
                    * np.exp(1j * self.theta_t[i])
                    * links.get_link(transmitter[0], self)[i]
                )
            # Start from i = elements_per_bs1 for the second half of the RIS
            for i in range(self.elements_per_bs1, self.elements):
                ris_2h_val += np.abs(
                    np.conj(links.get_link(self, receiver)[i - self.elements_per_bs1])
                    * np.sqrt(self.beta_t[i])
                    * np.exp(1j * self.theta_t[i])
                    * links.get_link(transmitter[1], self)[i - self.elements_per_bs1]
                )

            links.update_link(transmitter[0], receiver, ris_1h_val)
            links.update_link(transmitter[1], receiver, ris_2h_val)

        elif links.get_link_type(transmitter, receiver) == "1,c":
            ris_addition = np.zeros((links.size, 1), dtype=np.float64)

            for i in range(self.elements_per_bs1):
                ris_addition += np.abs(
                    np.conj(links.get_link(self, receiver)[i])
                    * np.sqrt(self.beta_r[i])
                    * np.exp(1j * self.theta_r[i])
                    * links.get_link(transmitter, self)[i]
                )

            links.update_link(transmitter, receiver, ris_addition)

        elif links.get_link_type(transmitter, receiver) == "2,c":
            ris_addition = np.zeros((links.size, 1), dtype=np.float64)

            for i in range(self.elements_per_bs1, self.elements):
                ris_addition += np.abs(
                    np.conj(links.get_link(self, receiver)[i - self.elements_per_bs1])
                    * np.sqrt(self.beta_r[i])
                    * np.exp(1j * self.theta_r[i])
                    * links.get_link(transmitter, self)[i - self.elements_per_bs1]
                )

            links.update_link(transmitter, receiver, ris_addition)

        else:
            raise NotImplementedError("Invalid link type.")


__all__ = ["STAR"]

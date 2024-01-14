from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

import numpy as np

from ...utils import wrapTo2Pi
from .system import SystemObject

if TYPE_CHECKING:
    from .link import LinkCollection


class STAR(SystemObject):
    """A class representing a STAR-RIS. Inherits from SystemObject. Passive in nature, can only reflect the incoming signal.

    Args:
        name: The name of the STAR-RIS.
        position: [x, y] coordinates of the STAR-RIS, [x, y, z] coordinates if 3D.
        elements: The number of elements in the RIS.
        beta_r: The reflection coefficients of the RIS. Defaults to 0.5.
        beta_t: The transmission coefficients of the RIS. Defaults to 0.5.
        custom_assignment: Custom assignment, i.e., different number of elements assigned to BS1 and BS2 or beta_r and beta_t other than halved.

    Attributes:
        name: Stores the name of the system object.
        position: Stores the [x, y] coordinates of the system object, [x, y, z] coordinates if 3D.
        elements: Stores the number of elements in the RIS.
        beta_r: Stores the reflection coefficients of the RIS.
        theta_r: Stores the phase shifts of the RIS.
        beta_t: Stores the transmission coefficients of the RIS.
        theta_t: Stores the phase shifts of the RIS.
        custom_assignment: Stores the custom assignment, i.e., different number of elements assigned to BS1 and BS2 or beta_r and beta_t other than halved.
        transmission_matrix: Stores the transmission matrix of the RIS.
        reflection_matrix: Stores the reflection matrix of the RIS.
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
            name: The name of the STAR-RIS.
            position: [x, y] coordinates of the STAR-RIS, [x, y, z] coordinates if 3D.
            elements: The number of elements in the RIS.
            beta_r: The reflection coefficients of the RIS. Defaults to 0.5.
            beta_t: The transmission coefficients of the RIS. Defaults to 0.5.
            custom_assignment: Custom assignment, i.e., different number of elements assigned to BS1 and BS2 or beta_r and beta_t other than halved.
        """

        super().__init__(name, position)
        if custom_assignment is None:
            assert elements % 2 == 0, "The number of elements must be even."
            self.elements = elements
            self.assignments = {"BS1": elements // 2, "BS2": elements // 2}
        else:
            assert isinstance(
                custom_assignment, dict
            ), "custom_assignment must be a dictionary."
            self.elements = elements
            self.assignments = custom_assignment
            assert self.assignments["BS1"] + self.assignments["BS2"] == self.elements, (
                "The number of elements in the RIS must be equal to the sum of"
                "the number of elements assigned to BS1 and BS2."
            )

        assert beta_r + beta_t == 1, "beta_r + beta_t must be equal to 1."

        self.beta_r = np.ones((self.elements, 1, 1)) * beta_r
        self.beta_t = np.ones((self.elements, 1, 1)) * beta_t

    def set_reflection_parameters(
        self,
        links: LinkCollection,
        transmitters: List[SystemObject],
        receivers: List[SystemObject],
    ) -> None:
        """Sets the reflection parameters of the RIS.

        Args:
            links: The collection of links in the system.
            transmitters: The list of transmitters in the system.
            receivers: The list of receivers in the system.

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

        self.theta_r[: self.assignments["BS1"]] = wrapTo2Pi(
            wrapTo2Pi(np.angle(bs1_u1c))
            - (wrapTo2Pi(np.angle(bs1_ris)) + wrapTo2Pi(np.angle(ris_u1c)))
        )
        self.theta_r[self.assignments["BS1"] :] = wrapTo2Pi(
            wrapTo2Pi(np.angle(bs2_u2c))
            - (wrapTo2Pi(np.angle(bs2_ris)) + wrapTo2Pi(np.angle(ris_u2c)))
        )

    def set_transmission_parameters(
        self,
        links: LinkCollection,
        transmitters: List[SystemObject],
        receiver: SystemObject,
    ) -> None:
        """Sets the transmission parameters of the RIS.

        Args:
            links: The collection of links in the system.
            transmitters: The list of transmitters in the system.
            receiver: The far receiver (UF) in the system.

        Raises:
            AssertionError: If there are not exactly 2 base stations.
        """
        assert len(transmitters) == 2, "There must be exactly 2 base stations."
        assert isinstance(
            receiver, SystemObject
        ), "The receiver must be a SystemObject."

        bs1_uf, bs2_uf = links.get_link(transmitters[0], receiver), links.get_link(
            transmitters[1], receiver
        )
        bs1_ris, bs2_ris = links.get_link(transmitters[0], receiver), links.get_link(
            transmitters[1], self
        )
        ris_uf = links.get_link(self, receiver)

        self.theta_t = np.zeros((self.elements, links.size, 1))

        self.theta_t[: self.assignments["BS1"]] = wrapTo2Pi(
            wrapTo2Pi(np.angle(bs1_uf))
            - (
                wrapTo2Pi(np.angle(bs1_ris))
                + wrapTo2Pi(np.angle(ris_uf[: self.assignments["BS1"]]))
            )
        )
        self.theta_t[self.assignments["BS1"] :] = wrapTo2Pi(
            wrapTo2Pi(np.angle(bs2_uf))
            - (
                wrapTo2Pi(np.angle(bs2_ris))
                + wrapTo2Pi(np.angle(ris_uf[self.assignments["BS1"] :]))
            )
        )

    def merge_link(
        self,
        links: LinkCollection,
        transmitter: Union[SystemObject, List[SystemObject]],
        receiver: SystemObject,
    ) -> None:
        """Updates the link between the transmitter and receiver with combined channel. Expects the arguments to be in the order as link is defined.

        Args:
            links: The collection of links in the system.
            transmitter: The transmitter(s) in the system. Pass a list of transmitters if link type between SystemObject and SystemObject is "E".
            receiver The receiver in the system.

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

            for i in range(self.assignments["BS1"]):
                ris_1h_val += np.abs(
                    np.conj(links.get_link(self, receiver)[i])
                    * np.sqrt(self.beta_t[i])
                    * np.exp(1j * self.theta_t[i])
                    * links.get_link(transmitter[0], self)[i]
                )
            # Start from i = assignments["BS1"] for the second half of the RIS
            for i in range(self.assignments["BS1"], self.elements):
                ris_2h_val += np.abs(
                    np.conj(links.get_link(self, receiver)[i - self.assignments["BS1"]])
                    * np.sqrt(self.beta_t[i])
                    * np.exp(1j * self.theta_t[i])
                    * links.get_link(transmitter[1], self)[i - self.assignments["BS1"]]
                )

            links.update_link(transmitter[0], receiver, ris_1h_val)
            links.update_link(transmitter[1], receiver, ris_2h_val)

        elif links.get_link_type(transmitter, receiver) == "1,c":
            ris_addition = np.zeros((links.size, 1), dtype=np.float64)

            for i in range(self.assignments["BS1"]):
                ris_addition += np.abs(
                    np.conj(links.get_link(self, receiver)[i])
                    * np.sqrt(self.beta_r[i])
                    * np.exp(1j * self.theta_r[i])
                    * links.get_link(transmitter, self)[i]
                )

            links.update_link(transmitter, receiver, ris_addition)

        elif links.get_link_type(transmitter, receiver) == "2,c":
            ris_addition = np.zeros((links.size, 1), dtype=np.float64)

            for i in range(self.assignments["BS1"], self.elements):
                ris_addition += np.abs(
                    np.conj(links.get_link(self, receiver)[i - self.assignments["BS1"]])
                    * np.sqrt(self.beta_r[i])
                    * np.exp(1j * self.theta_r[i])
                    * links.get_link(transmitter, self)[i - self.assignments["BS1"]]
                )

            links.update_link(transmitter, receiver, ris_addition)

        else:
            raise NotImplementedError("Invalid link type.")

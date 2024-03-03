from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Tuple, Union

import numpy as np
import numpy.typing as npt

from ..network import Link
from ..utils import ensure_list

if TYPE_CHECKING:
    from ..network import *

NDArrayFloat = npt.NDArray[np.floating[Any]]
NDArrayComplex = npt.NDArray[np.complexfloating[Any, Any]]


class SISOCollection:
    """Data store for SISO (single-input single-output) environments.

    SISO (single-input single-output) channels are the simplest type of
    channels. They are used to model the propagation of signals between
    transceivers each with a single antenna. Optionally, the link can be to a
    RIS, which inherently contains multiple elements.

    Stores the links between the trasnsceivers/RISs and allows for easy access
    to channel gains, angles, and other properties.

    Attributes:
        links: Dictionary of all links. Keys are tuples of the form
            (transceiver/RIS, transceiver/RIS).
        channel_gains: Dictionary of channel gains. Keys are tuples of the form
            (transceiver/RIS, transceiver/RIS).
    """

    def __init__(self, realizations: int):
        """Initialize a SISOChannels object.

        Args:
            realizations: Number of channel realizations.
        """
        self._links = {}
        self._channel_gains = {}

        self._realizations = realizations

    @property
    def realizations(self) -> int:
        """Return the number of channel realizations."""
        return self._realizations

    def add_link(
        self,
        nodes: List[Union[Transceiver, RIS]],
        fading_args: Union[dict[str, Any], List[dict[str, Any]]],
        pathloss_args: Union[dict[str, Any], List[dict[str, Any]]],
    ) -> None:
        """Add a link to the channel.

        Order of the nodes is important. The first node is the transmitter and
        the second node is the receiver. For example, if the link is from node A
        to node B, then nodes=[A, B].

        For when RISs are used, the first node is the transmitter, the second
        node is the RIS, and the third node is the receiver. For example, if the
        link is from node A to node B to node C, then nodes=[A, B, C].

        When adding an RIS-assisted link, the fading and path loss arguments can
        be either a list of length 2 or a single dictionary. In the former case,
        the first element of the list corresponds to the fading and path loss
        arguments between the tx and the RIS, and the RIS and the rx,
        respectively. In the latter case, the same fading and path loss
        arguments are used for both links.

        Args:
            nodes: List of transceivers/RISs.
            fading_args: Arguments for the fading model.
            pathloss_args: Arguments for the pathloss model.
        """

        if len(nodes) == 2:
            tx, rx = nodes

            if (tx.id, rx.id) in self._links:
                raise ValueError("Link already exists.")

            _link = Link(
                tx=tx,
                rx=rx,
                fading_args=fading_args,
                pathloss_args=pathloss_args,
                shape=(tx.n_antennas, rx.n_antennas, self.realizations),
            )

            self._links[(tx.id, rx.id)] = _link
            self._channel_gains[(tx.id, rx.id)] = _link.channel_gain

        elif len(nodes) == 3:
            tx, ris, rx = nodes

            if (tx.id, ris.id) in self._links:
                raise ValueError("Link already exists.")

            if (ris.id, rx.id) in self._links:
                raise ValueError("Link already exists.")

            fading_args = ensure_list(fading_args, length=2)
            pathloss_args = ensure_list(pathloss_args, length=2)

            tx_ris_link = Link(
                tx=tx,
                rx=ris,
                fading_args=fading_args[0],
                pathloss_args=pathloss_args[0],
                shape=(tx.n_antennas, ris.n_elements, self.realizations),
            )
            ris_rx_link = Link(
                tx=ris,
                rx=rx,
                fading_args=fading_args[1],
                pathloss_args=pathloss_args[1],
                shape=(ris.n_elements, rx.n_antennas, self.realizations),
            )

            self._links[(tx.id, ris.id)] = tx_ris_link
            self._links[(ris.id, rx.id)] = ris_rx_link

            self._channel_gains[(tx.id, ris.id)] = tx_ris_link.channel_gain
            self._channel_gains[(ris.id, rx.id)] = ris_rx_link.channel_gain

        else:
            raise ValueError("Invalid number of nodes. Must be 2 or 3.")

    def _get_link_attribute(
        self,
        nodes: str | Tuple[Union[Transceiver, RIS], Union[Transceiver, RIS]],
        str_repr: bool = True,
        attribute: str = "",
    ) -> Any:
        # Split the nodes if they are a string
        if str_repr:
            nodes = nodes.split("->")
            assert len(nodes) in [2, 3], "Invalid number of nodes. Must be 2 or 3."
            nodes = tuple(nodes)

        # Convert the nodes to their respective objects
        else:
            assert len(nodes) in [2, 3], "Invalid number of nodes. Must be 2 or 3."
            nodes = tuple([node.id for node in nodes])

        if attribute:
            return getattr(self._links[nodes], attribute)
        else:
            return self._links[nodes]

    def get_link(
        self,
        nodes: str | Tuple[Union[Transceiver, RIS], Union[Transceiver, RIS]],
        str_repr: bool = True,
    ) -> Link:
        """Return the link between the nodes.

        If str_repr is True, then the nodes must be a string of the form
        f"{node1.id}->{node2.id}". Otherwise, the nodes must be a list of the
        form [node1, node2]. Can also be a list of the form
        f"{node1.id}->{node2.id}->{node3.id}" or [node1, node2, node3] as in the
        case of an RIS-assisted link.

        Example input:
            >>> get_link("A->B") # Link from node A to node B
            >>> get_link(["A", "B"]) # Equivalent to the above

        Args:
            nodes: List of transceivers/RISs.
            str_repr: Whether to return a string representation of the nodes.

        Returns:
            Link between the nodes.
        """
        return self._get_link_attribute(nodes, str_repr)

    def get_channel_gain(
        self,
        nodes: str | Tuple[Union[Transceiver, RIS], Union[Transceiver, RIS]],
        str_repr: bool = True,
    ) -> NDArrayComplex:
        """Return the channel gain between the nodes.

        If str_repr is True, then the nodes must be a string of the form
        f"{node1.id}->{node2.id}". Otherwise, the nodes must be a list of the
        form [node1, node2]. Can also be a list of the form
        f"{node1.id}->{node2.id}->{node3.id}" or [node1, node2, node3] as in the
        case of an RIS-assisted link.

        Example input:
            >>> get_channel_gain("A->B") # Channel gain from node A to node B
            >>> get_channel_gain(["A", "B"]) # Equivalent to the above

        Args:
            nodes: List of transceivers/RISs.
            str_repr: Whether to return a string representation of the nodes.

        Returns:
            Channel gain between the nodes.
        """
        return self._get_link_attribute(nodes, str_repr, "channel_gain")

    def get_magnitude(
        self,
        nodes: str | Tuple[Union[Transceiver, RIS], Union[Transceiver, RIS]],
        str_repr: bool = True,
    ) -> NDArrayFloat:
        """Return the magnitude of the channel gain between the nodes.

        If str_repr is True, then the nodes must be a string of the form
        f"{node1.id}->{node2.id}". Otherwise, the nodes must be a list of the
        form [node1, node2]. Can also be a list of the form
        f"{node1.id}->{node2.id}->{node3.id}" or [node1, node2, node3] as in the
        case of an RIS-assisted link.

        Example input:
            >>> get_magnitude("A->B") # Magnitude from node A to node B
            >>> get_magnitude(["A", "B"]) # Equivalent to the above

        Args:
            nodes: List of transceivers/RISs.
            str_repr: Whether to return a string representation of the nodes.

        Returns:
            Magnitude of the channel gain between the nodes.
        """
        return np.abs(self._get_link_attribute(nodes, str_repr, "channel_gain"))

    def get_angle(
        self,
        nodes: str | Tuple[Union[Transceiver, RIS], Union[Transceiver, RIS]],
        str_repr: bool = True,
    ) -> NDArrayFloat:
        """Return the angle between the nodes.

        If str_repr is True, then the nodes must be a string of the form
        f"{node1.id}->{node2.id}". Otherwise, the nodes must be a list of the
        form [node1, node2]. Can also be a list of the form
        f"{node1.id}->{node2.id}->{node3.id}" or [node1, node2, node3] as in the
        case of an RIS-assisted link.

        Example input:
            >>> get_angle("A->B") # Angle from node A to node B
            >>> get_angle(["A", "B"]) # Equivalent to the above

        Args:
            nodes: List of transceivers/RISs.
            str_repr: Whether to return a string representation of the nodes.

        Returns:
            Angle between the nodes.
        """
        return np.angle(self._get_link_attribute(nodes, str_repr, "channel_gain"))

    def get_distance(
        self,
        nodes: str | Tuple[Union[Transceiver, RIS], Union[Transceiver, RIS]],
        str_repr: bool = True,
    ):
        """Return the distance between the nodes.

        If str_repr is True, then the nodes must be a string of the form
        f"{node1.id}->{node2.id}". Otherwise, the nodes must be a list of the
        form [node1, node2]. Can also be a list of the form
        f"{node1.id}->{node2.id}->{node3.id}" or [node1, node2, node3] as in the
        case of an RIS-assisted link.

        Example input:
            >>> get_distance("A->B") # Distance from node A to node B
            >>> get_distance(["A", "B"]) # Equivalent to the above

        Args:
            nodes: List of transceivers/RISs.
            str_repr: Whether to return a string representation of the nodes.

        Returns:
            Distance between the nodes.
        """
        return self._get_link_attribute(nodes, str_repr, "distance")


__all__ = ["SISOCollection"]

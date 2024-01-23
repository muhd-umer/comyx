from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Tuple, Union

import numpy as np
import numpy.typing as npt

from ..fading import get_rvs
from ..propagation import get_pathloss
from ..utils import db2pow, get_distance

if TYPE_CHECKING:
    from .ris import RIS
    from .transceiver import Transceiver

NDArrayFloat = npt.NDArray[np.floating[Any]]
NDArrayComplex = npt.NDArray[np.complexfloating[Any, Any]]


def ensure_list(arg, length=3):
    return arg if isinstance(arg, list) else [arg for _ in range(length)]


class Link:
    r"""Represents a link in the modelled environment.

    A link is a connection between two transceivers. It is characterized by the
    distance between the two transceivers, the path loss, and the channel gain.

    The path loss is the loss of signal strength due to the distance between the
    transceivers, and the channel gain is the gain of signal strength due to the
    channel between the transceivers.

    Mathematically, the channel gain is given by

    .. math::
        h_{\mathrm{tx,rx}} = g_{\mathrm{tx,rx}} \sqrt{PL(d_{\mathrm{tx,rx}})},

    where :math:`g_{\mathrm{tx,rx}}` is the small-scale fading (sampled from a
    distribution), :math:`PL(d_{\mathrm{tx,rx}})` is the path loss, and
    :math:`d_{\mathrm{tx,rx}}` is the distance between the transceivers.
    """

    def __init__(
        self,
        tx: Transceiver,
        rx: Transceiver,
        fading_args: dict[str, Any],
        pathloss_args: dict[str, Any],
        shape: Tuple[int, ...],
    ) -> None:
        """Initialize a link object.

        Args:
            tx: Transmitter of the link.
            rx: Receiver of the link.
            fading_args: Arguments for the fading model.
            pathloss_args: Arguments for the path loss model.
            shape: Number of shape for the channel gain.
        """

        self.tx = tx
        self.rx = rx
        self.fading_args = fading_args
        self.pathloss_args = pathloss_args
        self.shape = shape

        self.distance = self._distance()
        self.pathloss = self._pathloss()
        self.channel_gain = self._channel_gain()
        self.magnitude = np.abs(self.channel_gain)
        self.phase = np.angle(self.channel_gain)

    def _distance(self) -> float:
        """Calculate the distance between the nodes."""

        return get_distance(self.tx.position, self.rx.position)

    def _pathloss(self) -> NDArrayFloat:
        """Calculate the path loss."""

        return get_pathloss(self.distance, **self.pathloss_args)

    def _channel_gain(self) -> NDArrayComplex:
        """Calculate the channel gain."""

        rvs = get_rvs(self.shape, **self.fading_args)
        pathloss = db2pow(-self.pathloss)
        channel_gain = np.sqrt(pathloss) * rvs

        return channel_gain


class EffectiveLink(Link):
    r"""Represents an effective link in the modelled environment.

    An effective link is a connection between two transceivers through a RIS. It
    is characterized by the distance between the transceivers, the distance
    between the transceivers and the RIS, the distance between the RIS and the
    transceivers, the respective path losses, the cascaded channel gain, and the
    effective channel gain.

    The effective channel gain is the gain of signal strength due to the channel
    between the transceivers through the RIS, and the effective channel gain is
    the gain of signal strength due to the channel between the transceivers plus
    the effective channel gain.

    Mathematically, the effective channel gain is given by

    .. math::
        h_{\mathrm{eff}} = h_{\mathrm{tx,rx}} + \mathbf{h}_{\mathrm{ris,rx}}^H \mathbf{R} \mathbf{h}_{\mathrm{tx,ris}},

    where :math:`h_{\mathrm{tx,rx}}` is the channel gain between the
    transceivers, :math:`\mathbf{h}_{\mathrm{tx,ris}}` is the channel gain
    between the transceiver and the RIS, :math:`\mathbf{h}_{\mathrm{ris,rx}}` is
    the channel gain between the RIS and the receiver, and :math:`\mathbf{R}` is
    the reflection matrix of the RIS. The superscript :math:`H` denotes the
    Hermitian (complex conjugate) operator.
    """

    def __init__(
        self,
        tx: Transceiver,
        ris: RIS,
        rx: Transceiver,
        fading_args: Union[dict[str, Any], List[dict[str, Any]]],
        pathloss_args: Union[dict[str, Any], List[dict[str, Any]]],
        shape: Tuple[int, ...],
    ) -> None:
        """Initialize a cascaded link object.

        For fading and path loss arguments, either a list of length 3 or a
        single dictionary can be provided. In the former case, the first element
        of the list corresponds to the fading and path loss arguments between
        the tx and the rx, while the second and third elements correspond to the
        fading and path loss arguments between the tx and the ris, and the ris
        and the rx, respectively. In the latter case, the same fading and path
        loss arguments are used for all three links.

        Args:
            tx: Transmitter of the cascaded link.
            ris: RIS of the cascaded link.
            rx: Receiver of the cascaded link.
            fading_args: Arguments for the fading model.
            pathloss_args: Arguments for the path loss model.
            shape: Shape of the channel gain.
        """

        self.tx = tx
        self.ris = ris
        self.rx = rx

        self.fading_args = ensure_list(fading_args)
        self.pathloss_args = ensure_list(pathloss_args)

        assert len(self.fading_args) == 3 and len(self.pathloss_args) == 3, (
            "Fading and path loss arguments must be either a list of length 3 "
            "or a single dictionary."
        )

        self.shape = shape
        (
            self.distance_tx_rx,
            self.distance_tx_ris,
            self.distance_ris_rx,
        ) = self._distance()
        (
            self.pathloss_tx_rx,
            self.pathloss_tx_ris,
            self.pathloss_ris_rx,
        ) = self._pathloss()

        self.cascaded_channel_gain = self._cascaded_channel_gain()
        self.effective_channel_gain = self._effective_channel_gain()

        self.channel_gain = self.effective_channel_gain
        self.magnitude = np.abs(self.channel_gain)
        self.phase = np.angle(self.channel_gain)

    def _distance(self) -> Tuple[float, float, float]:
        """Calculate the distances between the nodes."""

        distance_tx_ris = get_distance(self.tx.position, self.ris.position)
        distance_ris_rx = get_distance(self.ris.position, self.rx.position)
        distance_tx_rx = get_distance(self.tx.position, self.rx.position)

        return distance_tx_ris, distance_ris_rx, distance_tx_rx

    def _pathloss(self) -> Tuple[NDArrayFloat, NDArrayFloat, NDArrayFloat]:
        """Calculate the path losses."""

        pathloss_tx_rx = get_pathloss(self.distance_tx_rx, **self.pathloss_args[0])
        pathloss_tx_ris = get_pathloss(self.distance_tx_ris, **self.pathloss_args[1])
        pathloss_ris_rx = get_pathloss(self.distance_ris_rx, **self.pathloss_args[2])

        return pathloss_tx_ris, pathloss_ris_rx, pathloss_tx_rx

    def _cascaded_channel_gain(self) -> NDArrayComplex:
        """Calculate the cascaded channel gain."""

        rvs_tx_ris = get_rvs(self.shape, **self.fading_args[1])
        rvs_ris_rx = get_rvs(self.shape, **self.fading_args[2])

        pathloss_tx_ris = db2pow(-self.pathloss_tx_ris)
        pathloss_ris_rx = db2pow(-self.pathloss_ris_rx)

        channel_gain_tx_ris = np.sqrt(pathloss_tx_ris) * rvs_tx_ris
        channel_gain_ris_rx = np.sqrt(pathloss_ris_rx) * rvs_ris_rx

        cascaded_channel_gain = (
            np.conj(channel_gain_ris_rx).T
            @ self.ris.reflection_matrix()
            @ channel_gain_tx_ris
        )

        return cascaded_channel_gain

    def _effective_channel_gain(self) -> NDArrayComplex:
        """Calculate the effective channel gain."""

        rvs_tx_rx = get_rvs(self.shape, **self.fading_args[0])

        pathloss_tx_rx = db2pow(-self.pathloss_tx_rx)
        channel_gain_tx_rx = np.sqrt(pathloss_tx_rx) * rvs_tx_rx

        effective_channel_gain = channel_gain_tx_rx + self.cascaded_channel_gain

        return effective_channel_gain


__all__ = ["Link", "EffectiveLink"]

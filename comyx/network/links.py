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

    Mathematically, the channel gain is given by

    .. math::
        h_{t,r} = g_{t,r} \sqrt{PL(d_{t,r})},

    where :math:`g_{t,r}` is the small-scale fading (sampled from a
    distribution), :math:`PL(d_{t,r})` is the path loss, and
    :math:`d_{t,r}` is the distance between the transceivers.

    Attributes:
        tx: Transmitter of the link.
        rx: Receiver of the link.
        shape: Number of shape for the channel gain.
        distance: Distance between the transceivers.
        pathloss: Path loss between the transceivers.
        channel_gain: Channel gain between the transceivers.
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
            shape: Shape for the channel gain matrix.
        """

        self.tx = tx
        self.rx = rx
        self._fading_args = fading_args
        self._pathloss_args = pathloss_args
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

        return get_pathloss(self.distance, **self._pathloss_args)

    def _channel_gain(self) -> NDArrayComplex:
        """Calculate the channel gain."""

        rvs = get_rvs(self.shape, **self._fading_args)
        pathloss = db2pow(-self.pathloss)
        channel_gain = np.sqrt(pathloss) * rvs

        return channel_gain


class RISLink(Link):
    r"""Represents an RIS link in the modelled environment.

    An RIS link is a connection between two transceivers through a RIS. It is
    characterized by the distance between the transceivers and the RIS, the
    distance between the RIS and the transceivers, the respective path losses,
    and the respective channel gains.

    *EffectiveLink does not compute either the cascaded channel gain or the
    effective channel gain implicitly since they require the optimization of the
    RIS reflection matrix. It is supposed to be a subcontainer for the possible
    channels between the transceivers and the RIS, and the RIS and the
    receivers.*

    Attributes:
        tx: Transmitter of the cascaded link.
        ris: RIS of the cascaded link.
        rx: Receiver of the cascaded link.
        shape: Number of shape for the channel gain matrix.
        distance: Dictionary containing distances between different components.
          Keys are 'tR' for transceiver and RIS, 'Rr' for RIS and receiver.
        pathloss: Dictionary containing path loss between different components.
          Keys are 'tR' for transceiver and RIS, 'Rr' for RIS and receiver.
        channel_gain: Dictionary containing channel gain between different components.
          Keys are 'tR' for transceiver and RIS, 'Rr' for RIS and receiver.
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

        For fading and path loss arguments, either a list of length 2 or a
        single dictionary can be provided. In the former case, the first element
        of the list corresponds to the fading and path loss arguments between
        the tx and the RIS, and the RIS and the rx, respectively. In the latter
        case, the same fading and path loss arguments are used for both links.

        Args:
            tx: Transmitter of the cascaded link.
            ris: RIS of the cascaded link.
            rx: Receiver of the cascaded link.
            fading_args: Arguments for the fading model.
            pathloss_args: Arguments for the path loss model.
            shape: Shape for the channel gain matrix.
        """

        self.tx = tx
        self.ris = ris
        self.rx = rx

        self._fading_args = ensure_list(fading_args)
        self._pathloss_args = ensure_list(pathloss_args)

        assert len(self._fading_args) == 2 and len(self._pathloss_args) == 2, (
            "Fading and path loss arguments must be either a list of length 2 "
            "or a single dictionary."
        )

        self.shape = shape
        self.distance = self._distance()
        self.pathloss = self._pathloss()
        self.channel_gain = self._channel_gain()

        self.magnitudes = {
            key: np.abs(value) for key, value in self.channel_gain.items()
        }
        self.phases = {key: np.angle(value) for key, value in self.channel_gain.items()}

    def _distance(self) -> dict[str, float]:
        """Calculate the distances between the nodes."""

        distance_tR = get_distance(self.tx.position, self.ris.position)
        distance_Rr = get_distance(self.ris.position, self.rx.position)

        return {"tR": distance_tR, "Rr": distance_Rr}

    def _pathloss(self) -> dict[str, NDArrayFloat]:
        """Calculate the path losses."""

        pathloss_tR = get_pathloss(self.distance["tR"], **self._pathloss_args[0])
        pathloss_Rr = get_pathloss(self.distance["Rr"], **self._pathloss_args[1])

        return {"tR": pathloss_tR, "Rr": pathloss_Rr}

    def _ris_channel_gain(self) -> Tuple[NDArrayComplex, NDArrayComplex]:
        """Calculate the cascaded channel gain."""

        rvs_tR = get_rvs(self.shape, **self._fading_args[0])
        rvs_Rr = get_rvs(self.shape, **self._fading_args[1])

        pathloss_tR = db2pow(-self.pathloss["tR"])
        pathloss_Rr = db2pow(-self.pathloss["Rr"])

        channel_gain_tR = np.sqrt(pathloss_tR) * rvs_tR
        channel_gain_Rr = np.sqrt(pathloss_Rr) * rvs_Rr

        return channel_gain_tR, channel_gain_Rr

    def _channel_gain(self) -> dict[str, NDArrayComplex]:
        """Calculate the channel gain."""

        channel_gain_tR, channel_gain_Rr = self._ris_channel_gain()

        return {
            "tR": channel_gain_tR,
            "Rr": channel_gain_Rr,
        }


def cascaded_channel_gain(ris_link: RISLink, style: str = "sum") -> NDArrayComplex:
    r"""Calculate the cascaded channel gain.

    The cascaded channel gain is the channel gain between the transceiver and
    the receiver through the RIS. Mathematically, the cascaded channel gain
    through the RIS is given by

    .. math::
        h_{csc}= \mathbf{h}_{R,r}^H \mathbf{R} \mathbf{h}_{t,R},

    where :math:`\mathbf{h}_{t,R}` is the channel gain between the transceiver
    and the RIS, :math:`\mathbf{h}_{R,r}` is the channel gain between the RIS
    and the receiver, and :math:`\mathbf{R}` is the reflection matrix of the
    RIS. The superscript :math:`H` denotes the Hermitian (complex conjugate)
    operator.

    If channel_gain_tR is of shape (Nt, K, Mc), and channel_gain_Rr is of shape
    (K, Nr, Mc), where Nt is the number of transmit antennas, K is the number of
    RIS elements, Nr is the number of receive antennas, and Mc is the number of
    channel realizations, then the cascaded channel gain is of shape (Nt, Nr,
    Mc). For SISO links, the cascaded channel gain is of shape (1, 1, Mc).

    Args:
        ris_link: RIS link.
        style: Formula used to calculate the cascaded channel gain.
          Possible values are 'sum' and 'matrix'.

    Returns:
        Cascaded channel gain.
    """

    channel_gain_tR = ris_link.channel_gain["tR"]
    channel_gain_Rr = ris_link.channel_gain["Rr"]

    if style == "sum":
        cascaded_channel_gain = np.sum(
            np.conj(channel_gain_Rr) * ris_link.ris.reflection_matrix * channel_gain_tR,
            axis=1,
        )

    elif style == "matrix":
        if channel_gain_tR.ndim != 2 or channel_gain_Rr.ndim != 2:
            raise NotImplementedError(
                "The matrix style is only implemented when the channel realization "
                + "dimension is absent. Use the sum style instead."
            )

        cascaded_channel_gain = (
            np.conj(channel_gain_Rr).T
            @ ris_link.ris.reflection_matrix
            @ channel_gain_tR
        )

    else:
        raise NotImplementedError(
            f"Style {style} not implemented. Possible values are 'sum' and 'matrix'."
        )

    return cascaded_channel_gain


def effective_channel_gain(
    direct_link: Link,
    cascaded_link: RISLink,
    style: str = "sum",
) -> NDArrayComplex:
    r"""Calculate the effective channel gain.

    The effective channel gain is the channel gain between the transceiver and
    the receiver through the RIS. Mathematically, the effective channel gain
    through the RIS is given by

    .. math::
        h_{eff}= h_{t,r} + \mathbf{h}_{R,r}^H \mathbf{R} \mathbf{h}_{t,R},

    where :math:`\mathbf{h}_{t,R}` is the channel gain between the transceiver
    and the RIS, :math:`\mathbf{h}_{R,r}` is the channel gain between the RIS
    and the receiver, :math:`\mathbf{R}` is the reflection matrix of the RIS,
    and :math:`h_{t,r}` is the channel gain between the transceiver and the
    receiver. The superscript :math:`H` denotes the Hermitian (complex
    conjugate) operator.

    Args:
        direct_link: Direct link.
        cascaded_link: Cascaded link.
        style: Formula used to calculate the cascaded channel gain.
          Possible values are 'sum' and 'matrix'.

    Returns:
        Effective channel gain.
    """

    channel_gain_tr = direct_link.channel_gain

    effective_channel_gain = channel_gain_tr + cascaded_channel_gain(
        cascaded_link, style=style
    )

    return effective_channel_gain


__all__ = ["cascaded_channel_gain", "effective_channel_gain", "Link", "RISLink"]

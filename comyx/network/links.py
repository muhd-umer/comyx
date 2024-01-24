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


class EffectiveLink(Link):
    r"""Represents an effective link in the modelled environment.

    An effective link is a connection between two transceivers through a RIS. It
    is characterized by the distance between the transceivers, the distance
    between the transceivers and the RIS, the distance between the RIS and the
    transceivers, the respective path losses, the cascaded channel gain, and the
    effective channel gain.

    Mathematically, the effective channel gain is given by

    .. math::
        h_{eff}= h_{t,r} + \mathbf{h}_{R,r}^H \mathbf{R} \mathbf{h}_{t,R},

    where :math:`h_{t,r}` is the channel gain between the
    transceivers, :math:`\mathbf{h}_{t,R}` is the channel gain
    between the transceiver and the RIS, :math:`\mathbf{h}_{R,r}` is
    the channel gain between the RIS and the receiver, and :math:`\mathbf{R}` is
    the reflection matrix of the RIS. The superscript :math:`H` denotes the
    Hermitian (complex conjugate) operator.

    *EffectiveLink does not compute either the cascaded channel gain or the
    effective channel gain since they require the optimization of the RIS
    reflection matrix. It is supposed to be a subcontainer for the possible
    channels between the transceivers and the RIS, and the RIS and the
    receivers.*

    Attributes:
        tx: Transmitter of the cascaded link.
        ris: RIS of the cascaded link.
        rx: Receiver of the cascaded link.
        shape: Number of shape for the channel gain matrix.
        distance: Dictionary containing distances between different components.
          Keys are 'tr' for transceivers, 'tR' for transceiver and RIS, 'Rr' for
          RIS and receiver.
        pathloss: Dictionary containing path loss between different components.
          Keys are 'tr' for transceivers, 'tR' for transceiver and RIS, 'Rr' for
          RIS and receiver.
        channel_gain: Dictionary containing channel gain between different components.
          Keys are 'tr' for transceivers, 'tR' for transceiver and RIS, 'Rr' for
          RIS and receiver.
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
        fading and path loss arguments between the tx and the RIS, and the RIS
        and the rx, respectively. In the latter case, the same fading and path
        loss arguments are used for all three links.

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

        assert len(self._fading_args) == 3 and len(self._pathloss_args) == 3, (
            "Fading and path loss arguments must be either a list of length 3 "
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

        distance_tr = get_distance(self.tx.position, self.rx.position)
        distance_tR = get_distance(self.tx.position, self.ris.position)
        distance_Rr = get_distance(self.ris.position, self.rx.position)

        return {"tr": distance_tr, "tR": distance_tR, "Rr": distance_Rr}

    def _pathloss(self) -> dict[str, NDArrayFloat]:
        """Calculate the path losses."""

        pathloss_tr = get_pathloss(self.distance["tr"], **self._pathloss_args[0])
        pathloss_tR = get_pathloss(self.distance["tR"], **self._pathloss_args[1])
        pathloss_Rr = get_pathloss(self.distance["Rr"], **self._pathloss_args[2])

        return {"tr": pathloss_tr, "tR": pathloss_tR, "Rr": pathloss_Rr}

    def _direct_channel_gain(self) -> NDArrayComplex:
        """Calculate the direct channel gain."""

        rvs_tr = get_rvs(self.shape, **self._fading_args[0])

        pathloss_tr = db2pow(-self.pathloss["tr"])
        channel_gain_tr = np.sqrt(pathloss_tr) * rvs_tr

        return channel_gain_tr

    def _ris_channel_gain(self) -> Tuple[NDArrayComplex, NDArrayComplex]:
        """Calculate the cascaded channel gain."""

        rvs_tR = get_rvs(self.shape, **self._fading_args[1])
        rvs_Rr = get_rvs(self.shape, **self._fading_args[2])

        pathloss_tR = db2pow(-self.pathloss["tR"])
        pathloss_Rr = db2pow(-self.pathloss["Rr"])

        channel_gain_tR = np.sqrt(pathloss_tR) * rvs_tR
        channel_gain_Rr = np.sqrt(pathloss_Rr) * rvs_Rr

        return channel_gain_tR, channel_gain_Rr

    def _channel_gain(self) -> dict[str, NDArrayComplex]:
        """Calculate the channel gain."""

        channel_gain_tr = self._direct_channel_gain()
        channel_gain_tR, channel_gain_Rr = self._ris_channel_gain()

        return {
            "tr": channel_gain_tr,
            "tR": channel_gain_tR,
            "Rr": channel_gain_Rr,
        }


__all__ = ["Link", "EffectiveLink"]

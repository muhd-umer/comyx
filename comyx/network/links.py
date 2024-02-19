from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Tuple, Union

import numpy as np
import numpy.typing as npt

from ..fading import get_rvs
from ..propagation import get_pathloss
from ..utils import db2pow, ensure_list, get_distance

if TYPE_CHECKING:
    from .ris import RIS
    from .transceiver import Transceiver

NDArrayFloat = npt.NDArray[np.floating[Any]]
NDArrayComplex = npt.NDArray[np.complexfloating[Any, Any]]


class Link:
    r"""Represents a link in the modelled environment.

    A link is a connection between two transceivers. It is characterized by the
    distance between the two transceivers, the path loss, and the channel gain.

    If rician_args are provided, the fading_args are used for the NLOS component
    and the rician_args are used for the LOS component.

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
    """

    def __init__(
        self,
        tx: Transceiver | RIS,
        rx: Transceiver | RIS,
        fading_args: dict[str, Any],
        pathloss_args: dict[str, Any],
        shape: Tuple[int, ...],
        rician_args: Union[dict[str, Any], None] = None,
        custom_rvs: Union[NDArrayComplex, None] = None,
        distance: Union[float, None] = None,
    ) -> None:
        """Initialize a link object.

        Args:
            tx: Transmitter of the link.
            rx: Receiver of the link.
            fading_args: Arguments for the fading model.
            pathloss_args: Arguments for the path loss model.
            shape: Shape for the channel gain matrix.
            rician_args: Arguments for the Rician fading model.
            custom_rvs: Custom random variables for the channel gain.
            distance: Distance between the transceivers.
        """

        self.tx = tx
        self.rx = rx
        self._fading_args = fading_args
        self._pathloss_args = pathloss_args
        self.shape = shape
        self._distance = (
            get_distance(self.tx.position, self.rx.position)
            if distance is None
            else distance
        )
        self._pathloss = get_pathloss(self.distance, **self._pathloss_args)

        if rician_args is not None:
            assert custom_rvs is None, (
                "The custom random variables cannot be provided when the fading "
                + "model is Rician."
            )
        self._rician_args = rician_args

        self._channel_gain = self.generate(custom_rvs)

    @property
    def distance(self) -> float:
        """Distance between the transceivers."""

        return self._distance

    @property
    def pathloss(self) -> NDArrayFloat:
        """Path loss between the transceivers."""

        return self._pathloss

    @property
    def channel_gain(self) -> NDArrayComplex:
        """Channel gain between the transceivers."""

        return self._channel_gain

    @property
    def magnitude(self) -> NDArrayFloat:
        """Magnitude of the channel"""

        return np.abs(self.channel_gain)

    @property
    def phase(self) -> NDArrayFloat:
        """Phase of the channel"""

        return np.angle(self.channel_gain)

    def generate(self, custom_rvs: NDArrayComplex | None = None) -> NDArrayComplex:
        """Generate channel gain between the transceivers.

        Not private to allow for the generation of new channel gains for more
        flexible simulations.
        """
        if custom_rvs is None:
            rvs = get_rvs(self.shape, **self._fading_args)

        elif self.rician:
            rvs = self.rician_fading(**self._rician_args)
        else:
            rvs = custom_rvs
            assert rvs.shape == self.shape, (
                "The shape of the custom random variables must be the same as the "
                + "shape of the channel gain."
            )

        pathloss = db2pow(-self.pathloss)
        channel_gain = np.sqrt(pathloss) * rvs

        return channel_gain

    def rician_fading(
        self,
        K: float,
        order: str = "post",
    ) -> NDArrayComplex:
        """Generate Rician fading channel gain between the transceivers.

        Args:
            K: Rician K-factor.
            pos_a: Position of the first transceiver.
            pos_b: Position of the second transceiver.
            order: Order of RIS in the link.
              Possible values are 'post' and 'pre'.

        Returns:
            Rician fading channel gain.
        """

        los = []
        if order == "post":
            assert isinstance(
                self.rx, RIS
            ), "The receiver must be an RIS for the post-order Rician fading."
            n_elements = self.rx.n_elements
        elif order == "pre":
            assert isinstance(
                self.tx, RIS
            ), "The transmitter must be an RIS for the pre-order Rician fading."
            n_elements = self.tx.n_elements
        else:
            raise ValueError(f"Order {order} not supported.")

        for m in range(n_elements):
            los.append(
                np.exp(
                    1j
                    * m
                    * np.pi
                    * (self.rx.position[1] - self.tx.position[1])
                    / (
                        np.sqrt(
                            (self.rx.position[0] - self.tx.position[0]) ** 2
                            + (self.rx.position[1] - self.tx.position[1]) ** 2
                        )
                    )
                )
            )

        los = np.array(los).reshape(self.shape)
        nlos = get_rvs(self.shape, **self._fading_args)
        rvs = los * (np.sqrt(K / (K + 1))) + nlos * (1 / (np.sqrt(K + 1)))

        return rvs

    def __repr__(self) -> str:
        return f"Link({self.tx.id}, {self.rx.id}) of shape {self.shape}"


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
    """

    def __init__(
        self,
        tx: Transceiver | RIS,
        ris: RIS,
        rx: Transceiver | RIS,
        fading_args: Union[dict[str, Any], List[dict[str, Any]]],
        pathloss_args: Union[dict[str, Any], List[dict[str, Any]]],
        shape: Tuple[Tuple[int, ...], Tuple[int, ...]],
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
            shape: Shape for the channel gain matrices.
        """

        self.tx = tx
        self.ris = ris
        self.rx = rx

        self._fading_args = ensure_list(fading_args, length=2)
        self._pathloss_args = ensure_list(pathloss_args, length=2)

        assert len(self._fading_args) == 2 and len(self._pathloss_args) == 2, (
            "Fading and path loss arguments must be either a list of length 2 "
            "or a single dictionary."
        )

        self.tR_shape, self.Rr_shape = shape
        self._distance_tR = get_distance(self.tx.position, self.ris.position)
        self._distance_Rr = get_distance(self.ris.position, self.rx.position)

        self._pathloss_tR = get_pathloss(self.distance["tR"], **self._pathloss_args[0])
        self._pathloss_Rr = get_pathloss(self.distance["Rr"], **self._pathloss_args[1])

        self._channel_gain_tR, self._channel_gain_Rr = self.generate()

    @property
    def distance(self) -> dict[str, float]:
        """Dictionary containing distances between different components.

        Keys are ``tR`` for transceiver and RIS, ``Rr`` for RIS and receiver.
        """

        return {"tR": self._distance_tR, "Rr": self._distance_Rr}

    @property
    def pathloss(self) -> dict[str, NDArrayFloat]:
        """Dictionary containing path loss between different components.

        Keys are ``tR`` for transceiver and RIS, ``Rr`` for RIS and receiver."""

        return {"tR": self._pathloss_tR, "Rr": self._pathloss_Rr}

    @property
    def channel_gain(self) -> dict[str, NDArrayComplex]:
        """Dictionary containing channel gain between different components.

        Keys are ``tR`` for transceiver and RIS, ``Rr`` for RIS and receiver."""

        return {
            "tR": self._channel_gain_tR,
            "Rr": self._channel_gain_Rr,
        }

    @property
    def magnitude(self) -> dict[str, NDArrayFloat]:
        """Dictionary containing magnitude of the channel between different components.

        Keys are ``tR`` for transceiver and RIS, ``Rr`` for RIS and receiver."""

        return {
            "tR": np.abs(self._channel_gain_tR),
            "Rr": np.abs(self._channel_gain_Rr),
        }

    @property
    def phase(self) -> dict[str, NDArrayFloat]:
        """Dictionary containing phase of the channel between different components.

        Keys are ``tR`` for transceiver and RIS, ``Rr`` for RIS and receiver."""

        return {
            "tR": np.angle(self._channel_gain_tR),
            "Rr": np.angle(self._channel_gain_Rr),
        }

    def generate(self) -> Tuple[NDArrayComplex, NDArrayComplex]:
        """Generate channels to and from the Transceiver and the RIS.

        Not private to allow for the generation of new channel gains for more
        flexible simulations.
        """

        rvs_tR = get_rvs(self.tR_shape, **self._fading_args[0])
        rvs_Rr = get_rvs(self.Rr_shape, **self._fading_args[1])

        pathloss_tR = db2pow(-self.pathloss["tR"])
        pathloss_Rr = db2pow(-self.pathloss["Rr"])

        channel_gain_tR = np.sqrt(pathloss_tR) * rvs_tR
        channel_gain_Rr = np.sqrt(pathloss_Rr) * rvs_Rr

        return channel_gain_tR, channel_gain_Rr


def cascaded_channel_gain(ris_link: RISLink, style: str = "sum") -> NDArrayComplex:
    r"""Calculate the cascaded channel gain.

    The cascaded channel gain is the channel gain between the transceiver and
    the receiver through the RIS. Mathematically, the cascaded channel gain
    through the RIS is given by

    .. math::
        h_{csc}= \mathbf{h}_{R,r}^T \mathbf{R} \mathbf{h}_{t,R},

    where :math:`\mathbf{h}_{t,R}` is the channel gain between the transceiver
    and the RIS, :math:`\mathbf{h}_{R,r}` is the channel gain between the RIS
    and the receiver, and :math:`\mathbf{R}` is the reflection matrix of the
    RIS. The superscript :math:`T` denotes the transpose operator.

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

    assert channel_gain_tR.shape[-1] == channel_gain_Rr.shape[-1], (
        "The number of channel  realizations must be the same for both channel "
        + "gains."
    )
    mc = channel_gain_tR.shape[-1]

    if style == "sum":
        cascaded_channel_gain = np.zeros(
            (ris_link.tx.n_antennas, ris_link.rx.n_antennas, mc), dtype=np.complex128
        )
        for i in range(ris_link.ris.n_elements):
            cascaded_channel_gain += (
                channel_gain_tR[:, i, :]
                * ris_link.ris.amplitudes[i]
                * np.exp(1j * ris_link.ris.phase_shifts[i])
                * channel_gain_Rr[i, :, :]
            )

    elif style == "matrix":
        if channel_gain_tR.ndim != 2 or channel_gain_Rr.ndim != 2:
            raise NotImplementedError(
                "The matrix style is only implemented when the channel realization "
                + "dimension is absent. Use the sum style instead."
            )

        cascaded_channel_gain = (
            channel_gain_Rr.T @ ris_link.ris.reflection_matrix @ channel_gain_tR
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
        h_{eff}= h_{t,r} + \mathbf{h}_{R,r}^T \mathbf{R} \mathbf{h}_{t,R},

    where :math:`\mathbf{h}_{t,R}` is the channel gain between the transceiver
    and the RIS, :math:`\mathbf{h}_{R,r}` is the channel gain between the RIS
    and the receiver, :math:`\mathbf{R}` is the reflection matrix of the RIS,
    and :math:`h_{t,r}` is the channel gain between the transceiver and the
    receiver. The superscript :math:`T` denotes the transpose operator.

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

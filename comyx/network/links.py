from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Tuple, Union

import numpy as np
import numpy.typing as npt

from ..fading import get_rvs
from ..propagation import get_pathloss
from ..utils import db2pow, ensure_list, get_distance
from .ris import RIS, STAR_RIS

if TYPE_CHECKING:
    from .transceiver import Transceiver

NDArrayFloat = npt.NDArray[np.floating[Any]]
NDArrayComplex = npt.NDArray[np.complexfloating[Any, Any]]

EPSILON = np.finfo(float).eps


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
        seed: Union[int, None] = None,
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
            seed: Seed for the random number generator.
        """

        self.tx = tx
        self.rx = rx
        self.seed = seed
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

        # initialize the channel gain
        self.generate_rvs(custom_rvs=custom_rvs, seed=self.seed)
        self.update_channel(ex_pathloss=True, ex_rvs=True)

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

    def generate_rvs(
        self, custom_rvs: NDArrayComplex | None = None, seed: int = None
    ) -> None:
        """Generate random variables for the channel gain.

        Not private to allow for the generation of new channel gains for more
        flexible simulations.
        """
        if custom_rvs is None and self._rician_args is None:
            self.rvs = get_rvs(self.shape, **self._fading_args, seed=seed)
        elif self._rician_args is not None:
            self.rvs = self.rician_fading(**self._rician_args)
        else:
            self.rvs = custom_rvs
            assert self.rvs.shape == self.shape, (
                "The shape of the custom random variables must be the same as the "
                + "shape of the channel gain."
            )

    def update_params(self, distance: Union[float, None] = None) -> None:
        """Update the parameters of the link.

        Args:
            distance: New distance between the transceivers.
        """
        self._distance = (
            get_distance(self.tx.position, self.rx.position)
            if distance is None
            else distance
        )
        self._pathloss = get_pathloss(self.distance, **self._pathloss_args)

    def update_channel(
        self,
        distance: Union[float, None] = None,
        custom_rvs: NDArrayComplex | None = None,
        ex_pathloss: bool = False,
        ex_rvs: bool = False,
        seed: Union[int, None] = None,
    ) -> None:
        """Update the channel gain.

        Args:
            distance: New distance between the transceivers.
            custom_rvs: New random variables for the channel gain.
            ex_pathloss: Whether to exclude distance-based params from the update.
            ex_rvs: Whether to exclude the random variables from the update.
            seed: Seed for the random number generator.
        """

        if not ex_pathloss:
            self.update_params(distance=distance)

        if not ex_rvs:
            # generate new random variables
            self.generate_rvs(custom_rvs=custom_rvs, seed=seed)

        pathloss = db2pow(-self.pathloss)
        self._channel_gain = np.sqrt(pathloss) * self.rvs

    def rician_fading(
        self,
        K: float,
        order: str = "post",
        ris: bool = True,
    ) -> NDArrayComplex:
        """Generate Rician fading channel gain between the transceivers.

        Args:
            K: Rician K-factor.
            pos_a: Position of the first transceiver.
            pos_b: Position of the second transceiver.
            order: Order of RIS in the link.
              Possible values are 'post' and 'pre'.
            ris: Whether to consider the RIS in the link.

        Returns:
            Rician fading channel gain.
        """

        assert self.tx.position is not None and self.rx.position is not None, (
            "Positions of the transceivers must be provided to generate the Rician "
            + "fading."
        )

        los = []

        if ris:
            if order == "post":
                assert isinstance(
                    self.rx, (RIS, STAR_RIS)
                ), "The receiver must be an RIS for the post-order Rician fading."
                n_elements = self.rx.n_elements
            elif order == "pre":
                assert isinstance(
                    self.tx, (RIS, STAR_RIS)
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
                        np.sqrt(  # EPSILON is a small value to avoid division by zero
                            (self.rx.position[0] - self.tx.position[0] + EPSILON) ** 2
                            + (self.rx.position[1] - self.tx.position[1] + EPSILON) ** 2
                        )
                    )
                )
            )

        los = np.array(np.repeat(los, self.shape[-1])).reshape(self.shape)
        nlos = get_rvs(self.shape, **self._fading_args, seed=self.seed)
        rvs = los * (np.sqrt(K / (K + 1))) + nlos * (1 / (np.sqrt(K + 1)))

        return rvs

    def __repr__(self) -> str:
        return f"Link({self.tx.id}, {self.rx.id}) of shape {self.shape}"


def cascaded_channel_gain(
    tR_link: Link, Rr_link: Link, style: str = "sum", ele_idx: int = 0
) -> NDArrayComplex:
    r"""Calculate the cascaded channel gain.

    The cascaded channel gain is the channel gain between the transmitter and
    the receiver through the RIS. Mathematically, the cascaded channel gain
    through the RIS is given by

    .. math::
        h_{csc}= \mathbf{h}_{R,r}^T \mathbf{R} \mathbf{h}_{t,R},

    where :math:`\mathbf{h}_{t,R}` is the channel gain between the transmitter
    and the RIS, :math:`\mathbf{h}_{R,r}` is the channel gain between the RIS
    and the receiver, and :math:`\mathbf{R}` is the reflection matrix of the
    RIS. The superscript :math:`T` denotes the transpose operator.

    If channel_gain_tR is of shape (Nt, K, Mc), and channel_gain_Rr is of shape
    (K, Nr, Mc), where Nt is the number of transmit antennas, K is the number of
    RIS elements, Nr is the number of receive antennas, and Mc is the number of
    channel realizations, then the cascaded channel gain is of shape (Nt, Nr,
    Mc). For SISO links, the cascaded channel gain is of shape (1, 1, Mc).

    Args:
        tR_link: Link between the transmitter and the RIS.
        Rr_link: Link between the RIS and the receiver.
        style: Formula used to calculate the cascaded channel gain.
            Possible values are 'sum' and 'matrix'.
        ele_idx: Index of the elements of RIS in channel gain matrix.

    Returns:
        Cascaded channel gain.
    """

    channel_gain_tR = tR_link.channel_gain
    channel_gain_Rr = Rr_link.channel_gain

    # RIS object of both links must be the same
    assert tR_link.rx == Rr_link.tx, (
        "The receiver of the first link must be the same as the transmitter of the "
        + "second link."
    )

    ris = tR_link.rx  # or Rr_link.tx

    assert channel_gain_tR.shape[-1] == channel_gain_Rr.shape[-1], (
        "The number of channel  realizations must be the same for both channel "
        + "gains."
    )
    mc = channel_gain_tR.shape[-1]

    if style == "sum":
        cascaded_channel_gain = np.zeros(
            (tR_link.tx.n_antennas, Rr_link.rx.n_antennas, mc), dtype=np.complex128
        )
        if ele_idx == 0:
            for i in range(ris.n_elements):
                cascaded_channel_gain += (
                    channel_gain_tR[i, :, :]
                    * ris.amplitudes[i]
                    * np.exp(1j * ris.phase_shifts[i])
                    * channel_gain_Rr[i, :, :]
                )

        elif ele_idx == 1:
            for i in range(ris.n_elements):
                cascaded_channel_gain += (
                    channel_gain_tR[:, i, :]
                    * ris.amplitudes[i]
                    * np.exp(1j * ris.phase_shifts[i])
                    * channel_gain_Rr[:, i, :]
                )
        else:
            raise ValueError(f"Element index {ele_idx} not supported.")

    elif style == "matrix":
        if channel_gain_tR.ndim != 2 or channel_gain_Rr.ndim != 2:
            raise NotImplementedError(
                "The matrix style is only implemented when the channel realization "
                + "dimension is absent. Use the sum style instead."
            )

        cascaded_channel_gain = (
            channel_gain_Rr.T @ ris.reflection_matrix @ channel_gain_tR
        )

    else:
        raise NotImplementedError(
            f"Style {style} not implemented. Possible values are 'sum' and 'matrix'."
        )

    return cascaded_channel_gain


def effective_channel_gain(
    tr_link: Link,
    tR_link: Link,
    Rr_link: Link,
    style: str = "sum",
    ele_idx: int = 0,
) -> NDArrayComplex:
    r"""Calculate the effective channel gain.

    The effective channel gain is the channel gain between the transceiver and
    the receiver through the RIS. Mathematically, the effective channel gain
    through the RIS is given by

    .. math::
        h_{eff}= h_{t,r} + \mathbf{h}_{R,r}^T \mathbf{R} \mathbf{h}_{t,R},

    where :math:`\mathbf{h}_{t,R}` is the channel gain between the transmitter
    and the RIS, :math:`\mathbf{h}_{R,r}` is the channel gain between the RIS
    and the receiver, :math:`\mathbf{R}` is the reflection matrix of the RIS,
    and :math:`h_{t,r}` is the channel gain between the transmitter and the
    receiver. The superscript :math:`T` denotes the transpose operator.

    Args:
        tr: Direct link.
        tR: Link between the transmitter and the RIS.
        Rr: Link between the RIS and the receiver.
        style: Formula used to calculate the cascaded channel gain.
          Possible values are 'sum' and 'matrix'.
        ele_idx: Index of the elements of RIS in channel gain matrix.

    Returns:
        Effective channel gain.
    """

    channel_gain_tr = tr_link.channel_gain

    effective_channel_gain = channel_gain_tr + cascaded_channel_gain(
        tR_link, Rr_link, style=style
    )

    return effective_channel_gain


__all__ = ["Link", "cascaded_channel_gain", "effective_channel_gain"]

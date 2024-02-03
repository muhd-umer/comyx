from __future__ import annotations

from typing import Any, List

import numpy as np
import numpy.typing as npt

NDArrayFloat = npt.NDArray[np.floating[Any]]
RVDistribution = Any
NDArrayComplex = npt.NDArray[np.complexfloating[Any, Any]]


class RIS:
    r"""Represent a reconfigurable intelligent surface (RIS).

    An RIS is a surface with a large number of elements that can be
    electronically controlled to reflect the incoming signal in a desired
    direction. The RIS is assumed to be a square surface with a uniform element
    spacing.

    Mathematically, the reflection matrix of the RIS is given by

    .. math::
        \mathbf{R} = \text{diag}(\mathbf{a} \odot \exp(j \mathbf{\Phi})),

    where :math:`\mathbf{a}` is the vector of amplitudes, :math:`\mathbf{\Phi}`
    is the vector of phase shifts, and :math:`\odot` is the Hadamard product.
    """

    def __init__(
        self,
        id_: str,
        position: List[float],
        n_elements: int,
    ):
        """Initialize an RIS object.

        Args:
            id_: Unique identifier of the RIS.
            position: Position of the RIS in the environment.
            n_elements: Number of elements of the RIS.
        """
        self._id = id_
        self._position = position
        self._n_elements = n_elements

    @property
    def id(self) -> str:
        """Return the unique identifier of the transceiver."""
        return self._id

    @property
    def position(self) -> List[float]:
        """Return the position of the transceiver in the environment."""
        return self._position

    @property
    def n_elements(self) -> int:
        """Return the number of antennas of the transceiver."""
        return self._n_elements

    @property
    def phase_shifts(self) -> NDArrayFloat:
        """Return the phase shifts of the RIS."""
        if not hasattr(self, "_phase_shifts"):
            raise ValueError("Phase shifts must be set before accessing.")
        return self._phase_shifts

    @phase_shifts.setter
    def phase_shifts(self, phase_shifts: NDArrayFloat) -> None:
        """Set the phase shifts of the RIS."""
        assert phase_shifts.shape[0] != (
            self.n_elements,
        ), "Phase shifts must be a vector of length equal to the number of elements."
        self._phase_shifts = phase_shifts

    @property
    def amplitudes(self) -> NDArrayFloat:
        """Return the amplitudes of the RIS."""
        if not hasattr(self, "_amplitudes"):
            raise ValueError("Amplitudes must be set before accessing.")
        return self._amplitudes

    @amplitudes.setter
    def amplitudes(self, amplitudes: NDArrayFloat) -> None:
        """Set the amplitudes of the RIS."""
        assert amplitudes.shape[0] != (
            self.n_elements,
        ), "Amplitudes must be a vector of length equal to the number of elements."
        self._amplitudes = amplitudes

    @property
    def reflection_matrix(self) -> NDArrayComplex:
        """Return the reflection matrix of the RIS.

        The reflection matrix is a diagonal matrix with the phase shifts and
        amplitudes as its diagonal elements. The phase shifts and amplitudes
        must be set before accessing the reflection matrix.

        The diagonality of the reflection matrix is due to the fact that the
        each element of the RIS reflects the incoming signal independently of
        the other elements.

        Returns:
            The reflection matrix of the RIS.
        """
        if not hasattr(self, "_phase_shifts"):
            raise ValueError("Phase shifts must be set before accessing.")
        if not hasattr(self, "_amplitudes"):
            raise ValueError("Amplitudes must be set before accessing.")

        assert self.phase_shifts.ndim == 1, (
            "Phase shifts must be a vector (design choice)."
            + " Use amplitude and shifts individually instead.",
        )

        return np.diag(self.amplitudes * np.exp(1j * self.phase_shifts))

    def __repr__(self) -> str:
        return (
            f"{self.id} at position("
            f"{', '.join(str(self.position[i]) for i in range(len(self.position)))})"
        )


__all__ = ["RIS"]

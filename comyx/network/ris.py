from __future__ import annotations

from typing import Any, List, Union

import numpy as np
import numpy.typing as npt

NDArrayFloat = npt.NDArray[np.floating[Any]]
RVDistribution = Any
NDArrayComplex = npt.NDArray[np.complexfloating[Any, Any]]


class RIS:
    r"""Represents a reconfigurable intelligent surface (RIS).

    An RIS is a surface with a large number of elements that can be
    electronically controlled to reflect the incoming signal in a desired
    direction.

    Mathematically, the reflection matrix of the RIS is given by

    .. math::
        \mathbf{R} = \text{diag}(\mathbf{a} \odot \exp(j \mathbf{\Phi})),

    where :math:`\mathbf{a}` is the vector of amplitudes, :math:`\mathbf{\Phi}`
    is the vector of phase shifts, and :math:`\odot` is the Hadamard product.
    """

    def __init__(
        self,
        id_: str,
        n_elements: int,
        position: Union[List[float], None] = None,
    ):
        """Initialize an RIS object.

        Args:
            id_: Unique identifier of the RIS.
            n_elements: Number of elements of the RIS.
            position: Position of the RIS in the environment.
        """
        self._id = id_
        self._position = position
        self._n_elements = n_elements

    @property
    def id(self) -> str:
        """Return the unique identifier of the RIS."""
        return self._id

    @property
    def position(self) -> List[float]:
        """Return the position of the RIS in the environment."""
        return self._position

    @position.setter
    def position(self, position: List[float]) -> None:
        """Set the position of the RIS in the environment."""
        self._position = position

    @property
    def n_elements(self) -> int:
        """Return the number of elements of the RIS."""
        return self._n_elements

    @property
    def phase_shifts(self) -> NDArrayFloat:
        """Return the phase shifts of the RIS."""
        return self._get_attribute("_phase_shifts")

    @phase_shifts.setter
    def phase_shifts(self, phase_shifts: NDArrayFloat) -> None:
        """Set the phase shifts of the RIS."""
        self._set_attribute("_phase_shifts", phase_shifts)

    @property
    def amplitudes(self) -> NDArrayFloat:
        """Return the amplitudes of the RIS."""
        return self._get_attribute("_amplitudes")

    @amplitudes.setter
    def amplitudes(self, amplitudes: NDArrayFloat) -> None:
        """Set the amplitudes of the RIS."""
        self._set_attribute("_amplitudes", amplitudes)

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
        return f"{self.id}(position={self.position}, n_elements={self.n_elements})"

    def _get_attribute(self, attr: str) -> NDArrayFloat:
        """Return the attribute of the RIS."""
        if not hasattr(self, attr):
            raise ValueError(f"{attr[1:]} must be set before accessing.")
        return getattr(self, attr)

    def _set_attribute(self, attr: str, value: NDArrayFloat) -> None:
        """Set the attribute of the RIS."""
        assert (
            value.shape[0] == self.n_elements
        ), f"{attr[1:]} must be a vector of length equal to the number of elements."
        setattr(self, attr, value)


class STAR_RIS:
    r"""Represents a STAR-RIS (Simultaneously Transmitting and Reflecting RIS).

    An STAR-RIS is a surface with a large number of elements that can be
    electronically controlled to reflect and transmit the incoming signal in a
    both spaces.

    Mathematically, the characteristic matrices of the STAR-RIS is given by

    .. math::
        \mathbf{R}^{n} = \text{diag}(\mathbf{a}^{n} \odot \exp(j \mathbf{\Phi}^{n})),

    where :math:`n \in \{t, r\}` and represents the transmission and reflection
    mode, respectively. Furthermore, $\mathbf{a}^{n}$ is the vector of
    amplitudes, :math:`\mathbf{\Phi}^{n}` is the vector of phase shifts, and $\odot$
    is the Hadamard product.

    Note that STAR-RIS must satisfy the law of conservation of energy, that is,
    :math:`\forall i \in \{1, \ldots, N\}` (where :math:`N` is the number of
    elements of the STAR-RIS), :math:`(a^{t}_{i})^2 + (a^{r}_{i})^2 = 1`.
    """

    def __init__(
        self,
        id_: str,
        n_elements: int,
        position: Union[List[float], None] = None,
    ):
        """Initialize a STAR-RIS object.

        Args:
            id_: Unique identifier of the STAR-RIS.
            n_elements: Number of both transmission and reflection elements of
              the STAR-RIS.
            position: Position of the STAR-RIS in the environment.
        """
        self._id = id_
        self._position = position
        self._n_elements = n_elements

    @property
    def id(self) -> str:
        """Return the unique identifier of the STAR-RIS."""
        return self._id

    @property
    def position(self) -> List[float]:
        """Return the position of the STAR-RIS in the environment."""
        return self._position

    @position.setter
    def position(self, position: List[float]) -> None:
        """Set the position of the STAR-RIS in the environment."""
        self._position = position

    @property
    def n_elements(self) -> int:
        """Return the number of antennas of the STAR-RIS."""
        return self._n_elements

    @property
    def reflection_phases(self) -> NDArrayFloat:
        """Return the reflection phase shifts of the STAR-RIS."""
        return self._get_attribute("_reflection_phases")

    @reflection_phases.setter
    def reflection_phases(self, reflection_phases: NDArrayFloat) -> None:
        """Set the reflection phase shifts of the STAR-RIS."""
        self._set_attribute("_reflection_phases", reflection_phases)

    @property
    def transmission_phases(self) -> NDArrayFloat:
        """Return the transmission phase shifts of the STAR-RIS."""
        return self._get_attribute("_transmission_phases")

    @transmission_phases.setter
    def transmission_phases(self, transmission_phases: NDArrayFloat) -> None:
        """Set the transmission phase shifts of the STAR-RIS."""
        self._set_attribute("_transmission_phases", transmission_phases)

    @property
    def reflection_amplitudes(self) -> NDArrayFloat:
        """Return the reflection amplitudes of the STAR-RIS."""
        return self._get_attribute("_reflection_amplitudes")

    @reflection_amplitudes.setter
    def reflection_amplitudes(self, reflection_amplitudes: NDArrayFloat) -> None:
        """Set the reflection amplitudes of the STAR-RIS."""
        self._set_attribute("_reflection_amplitudes", reflection_amplitudes)

    @property
    def transmission_amplitudes(self) -> NDArrayFloat:
        """Return the transmission amplitudes of the STAR-RIS."""
        return self._get_attribute("_transmission_amplitudes")

    @transmission_amplitudes.setter
    def transmission_amplitudes(self, transmission_amplitudes: NDArrayFloat) -> None:
        """Set the transmission amplitudes of the STAR-RIS."""
        self._set_attribute("_transmission_amplitudes", transmission_amplitudes)

    @property
    def reflection_matrix(self) -> NDArrayComplex:
        """Return the reflection matrix of the STAR-RIS.

        The reflection matrix is a diagonal matrix with the phase shifts and
        amplitudes as its diagonal elements. The phase shifts and amplitudes
        must be set before accessing the reflection matrix.

        The diagonality of the reflection matrix is due to the fact that the
        each element of the RIS reflects the incoming signal independently of
        the other elements.

        Returns:
            The reflection matrix of the RIS.
        """
        if not hasattr(self, "_reflection_shifts"):
            raise ValueError("Reflection phase shifts must be set before accessing.")
        if not hasattr(self, "_reflection_amplitudes"):
            raise ValueError("Reflection amplitudes must be set before accessing.")

        assert self.reflection_shifts.ndim == 1, (
            "Reflection phase shifts must be a vector (design choice)."
            + " Use amplitude and shifts individually instead.",
        )

        return np.diag(self.reflection_amplitudes * np.exp(1j * self.reflection_shifts))

    @property
    def transmission_matrix(self) -> NDArrayComplex:
        """Return the transmission matrix of the STAR-RIS.

        The transmission matrix is a diagonal matrix with the phase shifts and
        amplitudes as its diagonal elements. The phase shifts and amplitudes
        must be set before accessing the transmission matrix.

        The diagonality of the transmission matrix is due to the fact that the
        each element of the RIS reflects the incoming signal independently of
        the other elements.

        Returns:
            The transmission matrix of the STAR-RIS.
        """
        if not hasattr(self, "_transmission_shifts"):
            raise ValueError("Transmission phase shifts must be set before accessing.")
        if not hasattr(self, "_transmission_amplitudes"):
            raise ValueError("Transmission amplitudes must be set before accessing.")

        assert self.transmission_shifts.ndim == 1, (
            "Transmission phase shifts must be a vector (design choice)."
            + " Use amplitude and shifts individually instead.",
        )

        return np.diag(
            self.transmission_amplitudes * np.exp(1j * self.transmission_shifts)
        )

    def _get_attribute(self, attr: str) -> NDArrayFloat:
        """Return the attribute of the STAR-RIS."""
        if not hasattr(self, attr):
            raise ValueError(f"{attr[1:]} must be set before accessing.")
        return getattr(self, attr)

    def _set_attribute(self, attr: str, value: NDArrayFloat) -> None:
        """Set the attribute of the STAR-RIS."""
        assert (
            value.shape[0] == self.n_elements
        ), f"{attr[1:]} must be a vector of length equal to the number of elements."
        setattr(self, attr, value)

    def __repr__(self) -> str:
        return f"{self.id}(position={self.position}, n_elements={self.n_elements})"


__all__ = ["RIS", "STAR_RIS"]

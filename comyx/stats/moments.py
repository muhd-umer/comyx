from __future__ import annotations

from typing import Any, Tuple

import numpy as np
import numpy.typing as npt
from scipy.special import gamma

NDArrayFloat = npt.NDArray[np.floating[Any]]


def fun_mu_naka(
    p: int,
    m: float,
    omega: NDArrayFloat,
) -> NDArrayFloat:
    """Computes the p-th moment of the Nakagami-m distribution.

    Args:
        p: Order of the moment to compute.
        m: Shape parameter of the distribution.
        omega: Scale parameter of the distribution.

    Returns:
        The p-th moment of the Nakagami-m distribution.
    """
    return np.array((gamma(m + p / 2) / gamma(m)) * (m / omega) ** (-p / 2))


def fun_mu_gamma(
    p: int,
    k: float,
    theta: NDArrayFloat,
) -> NDArrayFloat:
    """Computes the p-th moment of the Gamma distribution.

    Args:
        p: Order of the moment to compute.
        k: Shape parameter of the distribution.
        theta: Scale parameter of the distribution.

    Returns:
        The p-th moment of the Gamma distribution.
    """
    return np.array((gamma(k + p) / gamma(k)) * (k / theta) ** (-p))


def fun_mu_doublenaka(
    p: int,
    m: float,
    k: float,
    omega: NDArrayFloat,
    theta: NDArrayFloat,
    c: float,
    N: int,
) -> NDArrayFloat:
    r"""Computes the p-th moment of the sum of two independent Nakagami-m RVs.

    .. math::
        G = \sqrt{c} \sum_{n=1}^{N} |{h_1}||{h_2}|

    , where :math:`h_1 \sim Nakagami(m, \Omega)` and :math:`h_2 \sim Nakagami(k,
    \theta)`.

    Args:
        p: Order of the moment to compute.
        m: Shape parameter of the first distribution :math:`h_1`.
        k: Shape parameter of the second distribution :math:`h_2`.
        omega: Scale parameter of the first distribution :math:`h_1`.
        theta: Scale parameter of the second distribution :math:`h_2`.
        c: Summation constant.
        N: Number of summation terms.

    Returns:
        The p-th moment of the sum of two independent Nakagami-m random
        variables.
    """
    return np.array(
        (
            gamma(m + (p / 2))
            * (np.sqrt(c) * N) ** p
            * gamma(k + (p / 2))
            * ((k * m) / (omega * theta)) ** (-p / 2)
        )
        / (gamma(k) * gamma(m))
    )


def fun_mu_effective(
    p: int,
    m_h: float,
    m_Ga: float,
    m_Gb: float,
    omega_h: NDArrayFloat,
    omega_Ga: NDArrayFloat,
    omega_Gb: NDArrayFloat,
    c: float,
    N: int,
):
    r"""Computes the p-th moment of the effective channel distribution.

    .. math::
        Z = |H|^2 = (h + G)^2

    , where :math:`h \sim Nakagami(m, \Omega)` and :math:`G \sim \Gamma(k_G,
    \theta_G)`. Furthermore, :math:`G` is defined as:

    .. math::
        G = \sqrt{c} \sum_{n=1}^{N} |{h_1}||{h_2}|

    Args:
        p: Order of the moment to compute. Only p = 1 and p = 2 are supported.
        m_h: Shape parameter of h distribution.
        m_Ga: Shape parameter of the first distribution of :math:`G`.
        m_Gb: Shape parameter of the second distribution of :math:`G`.
        omega_h: Scale parameter of h distribution.
        omega_Ga: Scale parameter of the first distribution of :math:`G`.
        omega_Gb: Scale parameter of the second distribution of :math:`G`.
        c: Summation constant.
        N: Number of summation terms.

    Returns:
        The p-th moment of the effective channel distribution.
    """
    assert p in [1, 2], "p must be 1 or 2, higher moments are not supported."

    if p == 1:
        return (
            fun_mu_doublenaka(2, m_Ga, m_Gb, omega_Ga, omega_Gb, c, N)
            + fun_mu_naka(2, m_h, omega_h)
            + (
                2
                * fun_mu_doublenaka(1, m_Ga, m_Gb, omega_Ga, omega_Gb, c, N)
                * fun_mu_naka(1, m_h, omega_h)
            )
        )
    else:
        return (
            fun_mu_doublenaka(4, m_Ga, m_Gb, omega_Ga, omega_Gb, c, N)
            + fun_mu_naka(4, m_h, omega_h)
            + (
                6
                * fun_mu_doublenaka(2, m_Ga, m_Gb, omega_Ga, omega_Gb, c, N)
                * fun_mu_naka(2, m_h, omega_h)
            )
            + (
                4
                * fun_mu_naka(3, m_h, omega_h)
                * fun_mu_doublenaka(1, m_Ga, m_Gb, omega_Ga, omega_Gb, c, N)
            )
            + (
                4
                * fun_mu_naka(1, m_h, omega_h)
                * fun_mu_doublenaka(3, m_Ga, m_Gb, omega_Ga, omega_Gb, c, N)
            )
        )


def approx_gamma_params(
    mu_1: NDArrayFloat,
    mu_2: NDArrayFloat,
    const: NDArrayFloat = np.array([1.0]),
) -> Tuple[NDArrayFloat, NDArrayFloat]:
    r"""Approximates the shape and scale of the Gamma distribution.

    Approximates the shape and scale parameters of the Gamma distribution
    given the first two moments of a non-negative RV. The approximation is
    based on the method of moments, given by:

    .. math::
        k = \frac{\mu^2}{\mu^{(2)} - \mu^2}

    .. math::
        \theta = \frac{\mu^{(2)} - \mu^2}{\mu}

    , where :math:`\mu` and :math:`\mu^{(2)}` are the first and second moments,
    respectively.

    Args:
        mu_1: First moment of the RV.
        mu_2: Second moment of the RV.
        const: Constant to multiply the scale parameter by.
          Defaults to 1.0.

    Returns:
        Shape and scale parameters of the Gamma distribution.
    """

    k = (mu_1**2) / (mu_2 - mu_1**2)
    theta = (mu_2 - mu_1**2) / mu_1

    return np.repeat(k, len(const)), theta * const


__all__ = [
    "fun_mu_naka",
    "fun_mu_gamma",
    "fun_mu_doublenaka",
    "fun_mu_effective",
    "approx_gamma_params",
]

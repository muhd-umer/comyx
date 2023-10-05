from typing import Any, Tuple

import numpy as np
import numpy.typing as npt
from scipy.special import gamma


def fun_mu_naka(
    p: int,
    m: float,
    omega: npt.NDArray[np.floating[Any]],
) -> npt.NDArray[np.floating[Any]]:
    """Computes the p-th moment of the Nakagami-m distribution.

    Args:
        p: The order of the moment.
        m: The shape parameter of the distribution.
        omega: The scale parameter of the distribution.

    Returns:
        The p-th moment of the Nakagami-m distribution.
    """
    return np.array((gamma(m + p / 2) / gamma(m)) * (m / omega) ** (-p / 2))


def fun_mu_gamma(
    p: int,
    k: float,
    theta: npt.NDArray[np.floating[Any]],
) -> npt.NDArray[np.floating[Any]]:
    """Computes the p-th moment of the Gamma distribution.

    Args:
        p: The order of the moment.
        k: The shape parameter of the distribution.
        theta: The scale parameter of the distribution.

    Returns:
        The p-th moment of the Gamma distribution.
    """
    return np.array((gamma(k + p) / gamma(k)) * (k / theta) ** (-p))


def fun_mu_doublenaka(
    p: int,
    m: float,
    k: float,
    omega: npt.NDArray[np.floating[Any]],
    theta: npt.NDArray[np.floating[Any]],
    c: float,
    N: int,
) -> npt.NDArray[np.floating[Any]]:
    r"""Computes the p-th moment of the sum of two independent Nakagami-m random variables.
        .. math::
            G = \sqrt{c} \sum_{n=1}^{N} |{h_1}||{h_2}|

    , where :math:`h_1 \sim Nakagami(m, \Omega)` and :math:`h_2 \sim Nakagami(k, \theta)`.

    Args:
        p: The order of the moment.
        m: The shape parameter of the first distribution.
        k: The shape parameter of the second distribution.
        omega: The scale parameter of the first distribution.
        theta: The scale parameter of the second distribution.
        c: Summation constant.
        N: The number of summation terms.

    Returns:
        The p-th moment of the sum of two independent Nakagami-m random variables.
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
    omega_h: npt.NDArray[np.floating[Any]],
    omega_Ga: npt.NDArray[np.floating[Any]],
    omega_Gb: npt.NDArray[np.floating[Any]],
    c: float,
    N: int,
):
    r"""Computes the p-th moment of the effective channel distribution.
        .. math::
            Z = |H|^2 = (h + G)^2

    , where :math:`h \sim Nakagami(m, \Omega)` and :math:`G \sim \Gamma(k_G, \theta_G)`.

    Args:
        p: The order of the moment.
        m_h: The shape parameter of h distribution.
        m_Ga: The shape parameter of the first distribution of G.
        m_Gb: The shape parameter of the second distribution of G.
        omega_h: The scale parameter of h distribution.
        omega_Ga: The scale parameter of the first distribution of G.
        omega_Gb: The scale parameter of the second distribution of G.
        c: Summation constant.
        N: The number of summation terms.

    Returns:
        The p-th moment of the effective channel distribution. Only p = 1 and p = 2 are supported.
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
    mu_1: npt.NDArray[np.floating[Any]],
    mu_2: npt.NDArray[np.floating[Any]],
    const: npt.NDArray[np.floating[Any]] = np.array([1.0]),
) -> Tuple[npt.NDArray[np.floating[Any]], npt.NDArray[np.floating[Any]]]:
    """Approximates the shape and scale parameters of the Gamma distribution given the first two moments.

    Args:
        mu_1: The first moment.
        mu_2: The second moment.
        const: The constant to multiply the scale parameter by. Defaults to 1.0.

    Returns:
        The shape and scale parameters of the Gamma distribution.
    """

    k = (mu_1**2) / (mu_2 - mu_1**2)
    theta = (mu_2 - mu_1**2) / mu_1

    return np.repeat(k, len(const)), theta * const


__all__ = [
    "fun_mu_naka",
    "fun_mu_doublenaka",
    "fun_mu_effective",
    "approx_gamma_params",
]

from __future__ import annotations

from typing import Any

import mpmath as mpm
import numpy as np
import numpy.typing as npt
from scipy.special import gamma

from ..utils import qfunc

NDArrayFloat = npt.NDArray[np.floating[Any]]
mpm.mp.dps = 10


def get_ergodic_rate(k: float, m: float, theta: float, omega: float) -> float:
    r"""Computes the ergodic rate of the system.

    .. math::
        \mathcal{R(k,m,\theta,\Omega)}=\frac{1}{{\log (2) \Gamma (k+m) B(k,m)}}{G_{3,3}^{3,2}\left(\frac{\Omega }{\theta }|\begin{array}{c}0,1-m,1 \\0,0,k \\\end{array}\right)}

    Args:
        k: Shape parameter of the numerator Gamma distribution.
        m: Shape parameter of the denominator Gamma distribution.
        theta: Scale parameter of the numerator Gamma distribution.
        omega: Scale parameter of the denominator Gamma distribution.

    Returns:
        The ergodic rate of the system.
    """
    assert not isinstance(k, np.ndarray), "mpmath does not operate on numpy arrays"
    return (1 / (mpm.log(2) * mpm.beta(k, m) * mpm.gamma(k + m))) * mpm.meijerg(
        [[0, 1 - m], [1]], [[0, 0, k], []], mpm.mpf(omega) / mpm.mpf(theta)
    )


def get_outage_lt(
    k: float, m: float, theta: float, omega: float, lambda_th: float
) -> float:
    r"""Computes the probability of the received SNR being less than the threshold.

    .. math::
        Pr(\lambda_{r}\lt\lambda_{th})=\frac{1}{{k B(k,m)}}{\left(\frac{10^{\lambda_{th} /10} \Omega}{\theta }\right)^k{_2F_1\left(k,k+m;k+1;-\frac{10^{\lambda_{th} /10} \Omega }{\theta}\right)}}

    , where :math:`\lambda_{r}=10\ln(x)`, with :math:`x \sim \beta'(k, m, \theta / \Omega)`.

    Args:
        k: Shape parameter of the numerator Gamma distribution.
        m: Shape parameter of the denominator Gamma distribution.
        theta: Scale parameter of the numerator Gamma distribution.
        omega: Scale parameter of the denominator Gamma distribution.
        lambda_th: Threshold of the received SNR.

    Returns:
        The outage probability of the system.
    """
    assert not isinstance(k, np.ndarray), "mpmath does not operate on numpy arrays"
    return (
        (((10 ** (lambda_th / 10) * omega) / theta) ** k)
        * mpm.hyp2f1(k, m + k, k + 1, -((10 ** (lambda_th / 10) * omega) / theta))
        / (k * mpm.beta(k, m))
    )


def get_outage_clt(
    k_a: float,
    m_a: float,
    theta_a: float,
    omega_a: float,
    k_b: float,
    m_b: float,
    theta_b: float,
    omega_b: float,
    lambda_a: float,
    lambda_b: float,
) -> float:
    r"""Computes the probability of inter-related SNRs.
    
    More specifically, it computes the probability of SNRs being greater than
    one threshold, but less than another.
    
    .. math::
        Pr(\lambda_{a}\gt\lambda_{th}, \lambda_{b}\lt\gamma_{th})=\frac{1}{k_b \Gamma\left(m_a\right) B\left(k_b,m_b\right)}{\left(\frac{10^{\gamma /10} \Omega _b}{\theta_b}\right){}^{k_b} {_2F_1\left(k_b,k_b+m_b;k_b+1;-\frac{10^{\gamma /10} \Omega_b}{\theta _b}\right)}} \\
        {\left(\Gamma \left(m_a\right)-\Gamma\left(k_a+m_a\right) \left(\frac{10^{\lambda /10} \Omega_a}{\theta _a}\right){}^{k_a} {_2\tilde{F}_1\left(k_a,k_a+m_a;k_a+1;-\frac{10^{\lambda /10}\Omega _a}{\theta _a}\right)}\right)}
            
    , where :math:`\lambda_{a}=10\ln(x)`, with :math:`x \sim \beta'(k_a, m_a, \theta_a / \Omega_a)` and :math:`\lambda_{b}=10\ln(y)`, with :math:`y \sim \beta'(k_b, m_b, \theta_b / \Omega_b)`.

    Args:
        k_a: Shape parameter of the numerator Gamma distribution of lambda_a.
        m_a: Shape parameter of the denominator Gamma distribution of lambda_a.
        theta_a: Scale parameter of the numerator Gamma distribution of 
          lambda_a.
        omega_a: Scale parameter of the denominator Gamma distribution of
          lambda_a.
        k_b: Shape parameter of the numerator Gamma distribution of lambda_b.
        m_b: Shape parameter of the denominator Gamma distribution of lambda_b.
        theta_b: Scale parameter of the numerator Gamma distribution of
          lambda_b.
        omega_b: Scale parameter of the denominator Gamma distribution of
          lambda_b.
        lambda_a: First threshold of the received SNR.
        lambda_b: Second threshold of the received SNR.

    Returns:
        The outage probability of the system.
    """
    return (
        (((10 ** (lambda_b / 10) * omega_b) / theta_b) ** k_b)
        * mpm.hyp2f1(
            k_b,
            m_b + k_b,
            k_b + 1,
            -((10 ** (lambda_b / 10) * omega_b) / theta_b),
        )
        / (k_b * mpm.beta(k_b, m_b))
    ) * (
        (
            gamma(m_a)
            - (
                gamma(m_a + k_a)
                * (((10 ** (lambda_a / 10) * omega_a) / theta_a) ** k_a)
                * (
                    (
                        mpm.hyp2f1(
                            k_a,
                            m_a + k_a,
                            k_a + 1,
                            -((10 ** (lambda_a / 10) * omega_a) / theta_a),
                        )
                    )
                    / (gamma(k_a + 1))
                )
            )
        )
        / (gamma(m_a))
    )


def get_outage_q(Pr: NDArrayFloat, threshold: float) -> NDArrayFloat:
    r"""Computes the outage probability of the system using the Q-function.

    The Q-function is defined as:

    .. math::
        Q(x)=\frac{1}{\sqrt{2 \pi}} \int_{x}^{\infty} e^{-\frac{u^{2}}{2}} d u

    Args:
        Pr: The received power of the system.
        threshold: The threshold of the received power.

    Returns:
        An array containing the outages of the system.
    """

    return qfunc((threshold - float(np.mean(Pr))) / float(np.std(Pr)))


__all__ = ["get_ergodic_rate", "get_outage_lt", "get_outage_clt", "get_outage_q"]

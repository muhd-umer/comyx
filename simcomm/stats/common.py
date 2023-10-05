from typing import Any, Tuple, Union

import numpy as np
import numpy.typing as npt
import scipy.stats as stats
from scipy.special import gamma

from .moments import approx_gamma_params


def approx_gamma_add_params(
    k_a: npt.NDArray[np.floating[Any]],
    k_b: npt.NDArray[np.floating[Any]],
    theta_a: npt.NDArray[np.floating[Any]],
    theta_b: npt.NDArray[np.floating[Any]],
) -> Tuple[npt.NDArray[np.floating[Any]], npt.NDArray[np.floating[Any]]]:
    """Computes the parameters of the sum of two independent Gamma random variables, given the shape and scale parameters of each distribution.

    Args:
        k_a: The shape parameter of the first Gamma distribution.
        k_b: The shape parameter of the second Gamma distribution.
        theta_a: The scale parameter of the first Gamma distribution.
        theta_b: The scale parameter of the second Gamma distribution.

    Returns:
        The shape and scale parameters of the sum of two independent Gamma random variables.
    """
    mu_1 = theta_a * k_a + theta_b * k_b
    mu_2 = (
        k_a * theta_a**2
        + k_a**2 * theta_a**2
        + k_b * theta_b**2
        + k_b**2 * theta_b**2
        + 2 * k_a * k_b * theta_a * theta_b
    )

    k = mu_1**2 / (mu_2 - mu_1**2)
    theta = (mu_2 - mu_1**2) / mu_1
    return np.array(k), np.array(theta)


def gamma_add_params(
    mu_a_1: npt.NDArray[np.floating[Any]],
    mu_a_2: npt.NDArray[np.floating[Any]],
    mu_b_1: npt.NDArray[np.floating[Any]],
    mu_b_2: npt.NDArray[np.floating[Any]],
    a: npt.NDArray[np.floating[Any]] = np.array([1.0]),
    b: npt.NDArray[np.floating[Any]] = np.array([1.0]),
) -> Tuple[npt.NDArray[np.floating[Any]], npt.NDArray[np.floating[Any]]]:
    """Computes the parameters of the sum of two independent Gamma random variables, given the first two moments of each distribution. The first distribution is optionally weighted by a, and the second by b.

    Args:
        mu_a_1: The first moment of the first Gamma distribution.
        mu_a_2: The second moment of the first Gamma distribution.
        mu_b_1: The first moment of the second Gamma distribution.
        mu_b_2: The second moment of the second Gamma distribution.
        a: The shape parameter of the first Gamma distribution.
        b: The shape parameter of the second Gamma distribution.

    Returns:
        The shape and scale parameters of the sum of two independent Gamma random variables.
    """

    mu_1 = (mu_a_1 * a) + (mu_b_1 * b)
    mu_2 = (a**2 * mu_a_2) + (b**2 * mu_b_2) + (2 * a * b * mu_a_1 * mu_b_1)

    return approx_gamma_params(mu_1, mu_2)


def gamma_plus_one_params(
    mu_a_1: npt.NDArray[np.floating[Any]],
    mu_a_2: npt.NDArray[np.floating[Any]],
) -> Tuple[npt.NDArray[np.floating[Any]], npt.NDArray[np.floating[Any]]]:
    """Computes the parameters of the sum of a Gamma random variable and one, given the first two moments of the Gamma distribution.

    Args:
        mu_a_1: The first moment of the Gamma distribution.
        mu_a_2: The second moment of the Gamma distribution.

    Returns:
        The shape and scale parameters of the sum of a Gamma random variable and one.
    """

    mu_1 = mu_a_1 + 1
    mu_2 = mu_a_2 + 2 * mu_a_1 + 1

    return approx_gamma_params(mu_1, mu_2)


def gamma_div_gamma_params(k_a, k_b, theta_a, theta_b):
    r"""Computes the parameters of the ratio of two independent Gamma random variables, given the shape and scale parameters of each distribution.
        .. math::
            z = \frac{h}{g}

    , where :math:`h \sim \Gamma(k_a, \theta_a)` and :math:`g \sim \Gamma(k_b, \theta_b)`. The resulting distribution is a Beta prime distribution, expressed as:
        .. math::
            z \sim \beta'(k_a, k_b, \theta_a / \theta_b)


    Args:
        k_a: The shape parameter of the first Gamma distribution.
        k_b: The shape parameter of the second Gamma distribution.
        theta_a: The scale parameter of the first Gamma distribution.
        theta_b: The scale parameter of the second Gamma distribution.

    Returns:
        A beta prime distribution with shape parameters k_a and k_b, and scale parameter theta_a / theta_b.
    """

    dist = stats.betaprime(k_a, k_b, loc=0, scale=theta_a / theta_b)
    return dist


__all__ = [
    "approx_gamma_add_params",
    "gamma_add_params",
    "gamma_plus_one_params",
    "gamma_div_gamma_params",
]

from __future__ import annotations

from typing import Any, Tuple

import numpy as np
import numpy.typing as npt
import scipy.stats as stats

from .moments import approx_gamma_params

NDArrayFloat = npt.NDArray[np.floating[Any]]
RVDistribution = Any


def gamma_add_params(
    mu_a_1: NDArrayFloat,
    mu_a_2: NDArrayFloat,
    mu_b_1: NDArrayFloat,
    mu_b_2: NDArrayFloat,
    a: NDArrayFloat = np.array([1.0]),
    b: NDArrayFloat = np.array([1.0]),
    return_type: str = "params",
) -> Tuple[NDArrayFloat, NDArrayFloat]:
    r"""Computes the parameters of the sum of two independent Gamma random variables.

    The first distribution is optionally weighted by a, and the second by b.

    .. math::
        z = a h + b g

    , where :math:`h \sim \Gamma(k_a, \theta_a)` and :math:`g \sim \Gamma(k_b,
    \theta_b)`. Also,

    .. math::
        k_n = \frac{\mu_{n,1}^{(2)}}{\mu_{n,2} - \mu_{n,1}^{(2)}}

    .. math::
        \theta_n = \frac{\mu_{n,2} - \mu_{n,1}^{(2)}}{\mu_{n,1}}

    , where :math:`n \in \{a, b\}`.

    The resulting distribution is a Gamma distribution, expressed as:

    .. math::
        z \sim \Gamma(k_z, \theta_z)

    Args:
        mu_a_1: First moment of the first Gamma distribution :math:`h`.
        mu_a_2: Second moment of the first Gamma distribution :math:`h`.
        mu_b_1: First moment of the second Gamma distribution :math:`g`.
        mu_b_2: Second moment of the second Gamma distribution :math:`g`.
        a: Shape parameter of the first Gamma distribution :math:`h`.
        b: Shape parameter of the second Gamma distribution :math:`g`.
        return_type: Return type of the function. Must be either "params" or
          "moments".

    Returns:
        Desired parameters of the sum of a Gamma random variable and one. If
        return_type is "params", returns the shape and scale parameters of the
        sum of two independent Gamma random variables. If return_type is
        "moments", returns the first two moments of the sum of two independent
        Gamma random variables.
    """

    mu_1 = (mu_a_1 * a) + (mu_b_1 * b)
    mu_2 = (a**2 * mu_a_2) + (b**2 * mu_b_2) + (2 * a * b * mu_a_1 * mu_b_1)

    if return_type == "params":
        return approx_gamma_params(mu_1, mu_2)
    elif return_type == "moments":
        return mu_1, mu_2
    else:
        raise ValueError("return_type must be either 'params' or 'moments'")


def gamma_plus_one_params(
    mu_a_1: NDArrayFloat,
    mu_a_2: NDArrayFloat,
    a: NDArrayFloat = np.array([1.0]),
    return_type: str = "params",
) -> Tuple[NDArrayFloat, NDArrayFloat]:
    r"""Computes the parameters of the sum of a Gamma random variable and one.

    .. math::
        z = h + 1

    , where :math:`h \sim \Gamma(k_a, \theta_a)`. Also,

    .. math::
        k_a = \frac{\mu_{a,1}^{(2)}}{\mu_{a,2} - \mu_{a,1}^{(2)}}

    .. math::
        \theta_a = \frac{\mu_{a,2} - \mu_{a,1}^{(2)}}{\mu_{a,1}}

    Args:
        mu_a_1: First moment of the Gamma distribution.
        mu_a_2: Second moment of the Gamma distribution.
        return_type: Return type of the function. Must be either "params" or
          "moments".

    Returns:
        Desired parameters of the sum of a Gamma random variable and one. If
        return_type is "params", returns the shape and scale parameters of the
        sum of a Gamma random variable and one. If return_type is "moments",
        returns the first two moments of the sum of a Gamma random variable and
        one.
    """

    mu_1 = (a * mu_a_1) + 1
    mu_2 = (a**2 * mu_a_2) + (2 * a * mu_a_1) + 1

    if return_type == "params":
        return approx_gamma_params(mu_1, mu_2)
    elif return_type == "moments":
        return mu_1, mu_2
    else:
        raise ValueError("return_type must be either 'params' or 'moments'")


def gamma_div_gamma_dist(
    k_a: NDArrayFloat, k_b: NDArrayFloat, theta_a: NDArrayFloat, theta_b: NDArrayFloat
) -> RVDistribution:
    r"""Computes the parameters of the ratio of two independent Gamma random variables.

    .. math::
        z = \frac{h}{g}

    , where :math:`h \sim \Gamma(k_a, \theta_a)` and :math:`g \sim \Gamma(k_b,
    \theta_b)`. The resulting distribution is a Beta prime distribution,
    expressed as:

    .. math::
        z \sim \beta'(k_a, k_b, \theta_a / \theta_b)

    Args:
        k_a: Shape parameter of the first Gamma distribution :math:`h`.
        k_b: Shape parameter of the second Gamma distribution :math:`g`.
        theta_a: Scale parameter of the first Gamma distribution :math:`h`.
        theta_b: Scale parameter of the second Gamma distribution :math:`g`.

    Returns:
        A beta prime distribution with shape parameters k_a and k_b, and scale
        parameter theta_a / theta_b.
    """

    dist = stats.betaprime(k_a, k_b, loc=0, scale=theta_a / theta_b)
    return dist


__all__ = [
    "gamma_add_params",
    "gamma_plus_one_params",
    "gamma_div_gamma_dist",
]

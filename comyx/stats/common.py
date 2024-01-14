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
    r"""Computes the parameters of the sum of two independent Gamma random variables, given the first two moments of each distribution. The first distribution is optionally weighted by a, and the second by b.

    .. math::
        z = a h + b g

    , where :math:`h \sim \Gamma(k_a, \theta_a)` and :math:`g \sim \Gamma(k_b, \theta_b)`. Also,

    .. math::
        k_n = \frac{\mu_{n,1}^{(2)}}{\mu_{n,2} - \mu_{n,1}^{(2)}}
    .. math::
        \theta_n = \frac{\mu_{n,2} - \mu_{n,1}^{(2)}}{\mu_{n,1}}

    , where :math:`n \in \{a, b\}`.

    The resulting distribution is a Gamma distribution, expressed as:

    .. math::
        z \sim \Gamma(k_z, \theta_z)

    Args:
        mu_a_1: The first moment of the first Gamma distribution.
        mu_a_2: The second moment of the first Gamma distribution.
        mu_b_1: The first moment of the second Gamma distribution.
        mu_b_2: The second moment of the second Gamma distribution.
        a: The shape parameter of the first Gamma distribution.
        b: The shape parameter of the second Gamma distribution.
        return_type: The type of the returned value. If "params", returns the shape and scale parameters of the sum of two independent Gamma random variables. If "moments", returns the first two moments of the sum of two independent Gamma random variables.

    Returns:
        The desired parameters of the sum of two independent Gamma random variables.
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
    r"""Computes the parameters of the sum of a Gamma random variable and one, given the first two moments of the Gamma distribution.

    .. math::
        z = h + 1

    , where :math:`h \sim \Gamma(k_a, \theta_a)`. Also,

    .. math::
        k_a = \frac{\mu_{a,1}^{(2)}}{\mu_{a,2} - \mu_{a,1}^{(2)}}

    .. math::
        \theta_a = \frac{\mu_{a,2} - \mu_{a,1}^{(2)}}{\mu_{a,1}}

    Args:
        mu_a_1: The first moment of the Gamma distribution.
        mu_a_2: The second moment of the Gamma distribution.
        return_type: The type of the returned value. If "params", returns the shape and scale parameters of the sum of a Gamma random variable and one. If "moments", returns the first two moments of the sum of a Gamma random variable and one.

    Returns:
        The desired parameters of the sum of a Gamma random variable and one.
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


# def approx_gamma_add_params(
#     k_a: NDArrayFloat,
#     k_b: NDArrayFloat,
#     theta_a: NDArrayFloat,
#     theta_b: NDArrayFloat,
#     return_type: str = "params",
# ) -> Tuple[NDArrayFloat, NDArrayFloat]:
#     """Computes the parameters of the sum of two independent Gamma random variables, given the shape and scale parameters of each distribution.

#     Args:
#         k_a: The shape parameter of the first Gamma distribution.
#         k_b: The shape parameter of the second Gamma distribution.
#         theta_a: The scale parameter of the first Gamma distribution.
#         theta_b: The scale parameter of the second Gamma distribution.
#         return_type: The type of the returned value. If "params", returns the shape and scale parameters of the sum of two independent Gamma random variables. If "moments", returns the first two moments of the sum of two independent Gamma random variables.

#     Returns:
#         The desired parameters of the sum of two independent Gamma random variables.
#     """
#     mu_1 = theta_a * k_a + theta_b * k_b
#     mu_2 = (
#         k_a * theta_a**2
#         + k_a**2 * theta_a**2
#         + k_b * theta_b**2
#         + k_b**2 * theta_b**2
#         + 2 * k_a * k_b * theta_a * theta_b
#     )

#     if return_type == "params":
#         return approx_gamma_params(mu_1, mu_2)
#     elif return_type == "moments":
#         return mu_1, mu_2
#     else:
#         raise ValueError("return_type must be either 'params' or 'moments'")


__all__ = [
    # "approx_gamma_add_params",
    "gamma_add_params",
    "gamma_plus_one_params",
    "gamma_div_gamma_dist",
]

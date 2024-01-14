from __future__ import annotations

from typing import Any, Tuple, Union

import numpy as np
import numpy.typing as npt
import scipy.stats as stats
from scipy.special import gamma

NDArrayFloat = npt.NDArray[np.floating[Any]]


class Nakagami:
    r"""The Nakagami distribution or the Nakagami-m distribution is a probability distribution related to the gamma distribution. The family of Nakagami distributions has two parameters: a shape parameter :math:`m` with :math:`m\geq 1/2` and a second parameter controlling spread :math:`\Omega > 0`.

    Density Function
        .. math::
            f(x; m, \Omega) = \frac{2m^m}{\Gamma(m)\Omega^m} x^{2m - 1} \exp\left(-\frac{m}{\Omega}x^2\right)

    , where :math:`\Gamma(.)` is the gamma function.

    Expected value
        .. math::
            \sqrt{\frac{\Omega}{m}} \frac{\Gamma\left(m + \frac{1}{2}\right)}{\Gamma(m)}


    Variance
        .. math::
            \Omega \left(1 - \frac{1}{m}\left(\frac{\Gamma\left(m + \frac{1}{2}\right)}{\Gamma(m)}\right)^2\right)

    Attributes:
        m: The shape parameter, which is the fading severity.
        omega: The scale parameter, which controls the spread of the distribution.

    Reference:
        https://en.wikipedia.org/wiki/Nakagami_distribution
    """

    def __init__(self, m: float, omega: float = 1) -> None:
        """Initialize the Nakagami distribution with the given parameters.

        Args:
            m: The shape parameter, which is the fading severity.
            omega: The scale parameter, which controls the spread of the distribution.
        """
        assert m >= 0.5, "The shape parameter must be greater than or equal to 0.5."
        assert omega > 0, "The scale parameter must be greater than 0."
        self.m = m
        self.omega = omega

    def pdf(self, x: NDArrayFloat) -> NDArrayFloat:
        """Return the probability density function of the Nakagami distribution.

        Args:
            x: The value at which to evaluate the probability density function.

        Returns:
            The probability density function evaluated at x.
        """
        return (
            2
            * self.m**self.m
            / (gamma(self.m) * self.omega**self.m)
            * x ** (2 * self.m - 1)
            * np.exp(-self.m * x**2 / self.omega)
        )

    def cdf(self, x: NDArrayFloat) -> NDArrayFloat:
        """Return the cumulative distribution function of the Nakagami distribution.

        Args:
            x: The value at which to evaluate the cumulative distribution

        Returns:
            The cumulative distribution function evaluated at x.
        """
        return stats.nakagami.cdf(x, self.m, scale=np.sqrt(self.omega))

    def expected_value(self) -> float:
        """Return the expected value of the Nakagami distribution.

        Returns:
            The expected value of the Nakagami distribution.
        """
        return gamma(self.m + 1 / 2) / gamma(self.m) * np.sqrt(self.omega / self.m)

    def variance(self) -> float:
        """Return the variance of the Nakagami distribution.

        Returns:
            The variance of the Nakagami distribution.
        """
        return self.omega * (
            1 - 1 / self.m * (gamma(self.m + 1 / 2) / gamma(self.m)) ** 2
        )

    def get_samples(self, size: Union[int, Tuple[int, ...]]) -> NDArrayFloat:
        """Generate random variables from the Nakagami distribution.

        Args:
            size: The number of random variables to generate.

        Returns:
            An array of size `size` containing random variables from the Nakagami distribution.
        """
        return np.array(
            stats.nakagami.rvs(self.m, scale=np.sqrt(self.omega), size=size)
        )

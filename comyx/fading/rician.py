from __future__ import annotations

from typing import Any, Tuple, Union

import numpy as np
import numpy.typing as npt
import scipy.stats as stats
from scipy.special import i0

from ..utils import laguerre

NDArrayFloat = npt.NDArray[np.floating[Any]]


class Rician:
    r"""Represents the :math:`\text{Rician}(K, \sigma)` distribution.

    The Rice distribution or Rician distribution (or, less commonly, Ricean
    distribution) is the probability distribution of the magnitude of a
    circularly-symmetric bivariate normal random variable, possibly with
    non-zero mean (noncentral).

    Density Function
        .. math::
            f(x; \nu, \sigma) = \frac{x}{\sigma^2} \exp\left(-\frac{x^2 + \nu^2}{2\sigma^2}\right) I_0\left(\frac{x\nu}{\sigma^2}\right)

    , where :math:`I_0` is the modified Bessel function of the first kind.

    Expected value
        .. math::
            \sigma \sqrt{\frac{\pi}{2}} \exp\left(-\frac{\nu^2}{2\sigma^2}\right)

    Variance
        .. math::
            2\sigma^2 + \nu^2 - \frac{\pi\sigma^2}{2}

    RMS value
        .. math::
            \sigma \sqrt{2 + \frac{\pi}{2}}

    Reference:
        https://en.wikipedia.org/wiki/Rice_distribution
    """

    def __init__(self, K: float, sigma: float = 1) -> None:
        """Initialize the Rician distribution with the given parameters.

        Args:
            K: Rician factor, i.e., ratio between the power of direct path and
            the power of scattered paths.
            sigma: The scale parameter, which is the standard deviation of the
              distribution.
        """
        self.K = K
        self.sigma = sigma
        self.omega = (2 * self.K + 2) * self.sigma**2
        self.nu = np.sqrt((K / (1 + K)) * self.omega)

    def pdf(self, x: NDArrayFloat) -> NDArrayFloat:
        """Probability density function of the Rician distribution.

        Args:
            x: Value at which pdf is evaluated.

        Returns:
            Value of the probability density function evaluated at x.
        """
        return (
            (x / self.sigma**2)
            * np.exp(-(x**2 + self.nu**2) / (2 * self.sigma**2))
            * i0(x * self.nu / self.sigma**2)
        )

    def cdf(self, x: NDArrayFloat) -> NDArrayFloat:
        """Cumulative distribution function of the the Rician distribution.

        Args:
            x: Value at which cdf is evaluated.

        Returns:
            Value of the cumulative distribution function evaluated at x.
        """
        return stats.rice.cdf(x, self.nu / self.sigma)

    def expected_value(self) -> float:
        """Returns the expected value of the Rician distribution."""
        arg = -self.nu**2 / (2 * self.sigma**2)
        return self.sigma * np.sqrt(np.pi / 2) * laguerre(arg, 1 / 2)

    def variance(self) -> float:
        """Returns the variance of the Rician distribution."""
        arg = -self.nu**2 / (2 * self.sigma**2)
        return (
            2 * self.sigma**2
            + self.nu**2
            - ((np.pi * self.sigma**2 / 2) * (laguerre(arg, 1 / 2) ** 2))
        )

    def rms_value(self) -> float:
        """Returns the RMS value of the Rician distribution."""
        return self.sigma * np.sqrt(2 + np.pi / 2)

    def get_samples(
        self, size: Union[int, Tuple[int, ...]], seed: int = None
    ) -> NDArrayFloat:
        """Generate random variables from the Rician distribution.

        Args:
            size: Nnumber of random variables to generate.
            seed: Seed for the random number generator.

        Returns:
            An array of size `size` containing random variables from the Rician
            distribution.
        """
        return np.array(
            stats.rice.rvs(
                self.nu / self.sigma, scale=self.sigma, size=size, random_state=seed
            )
        )


__all__ = ["Rician"]

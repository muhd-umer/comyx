from __future__ import annotations

from typing import Any, Tuple, Union

import numpy as np
import numpy.typing as npt
import scipy.stats as stats

NDArrayFloat = npt.NDArray[np.floating[Any]]
NDArraySigned = npt.NDArray[np.signedinteger[Any]]


class Rayleigh:
    r"""Represents the :math:`\text{Rayleigh}(\sigma)` distribution.

    The Rayleigh distribution is a continuous probability distribution for
    nonnegative-valued random variables. Up to rescaling, it coincides with
    the chi distribution with two degrees of freedom.

    Density function
        .. math::
            f(x; \sigma) = \frac{x}{\sigma^2} \cdot \exp\left(-\frac{x^2}{2\sigma^2}\right)

    Expected value
        .. math::
            \sigma \cdot \sqrt{\frac{\pi}{2}}

    Variance
        .. math::
            \left(2 - \frac{\pi}{2}\right) \cdot \sigma^2

    RMS value
        .. math::
            \sqrt{2} \cdot \sigma

    Reference:
        https://en.wikipedia.org/wiki/Rayleigh_distribution
    """

    def __init__(self, sigma: float = 1) -> None:
        """Initializes a Rayleigh distribution with the given scale parameter.

        Args:
            sigma: Scale parameter of the Rayleigh distribution. It must be
              greater than 0.
        """
        self.sigma = sigma

    def pdf(self, x: NDArrayFloat) -> NDArrayFloat:
        """Probability density function of the Rayleigh distribution.

        Args:
            x: Value at which pdf is evaluated.

        Returns:
            Value of the probability density function evaluated at x.
        """
        return (x / self.sigma**2) * np.exp(-(x**2) / (2 * self.sigma**2))

    def cdf(self, x: NDArrayFloat) -> NDArraySigned:
        """Cumulative distribution function of the Rayleigh distribution.

        Args:
            x: Value at which cdf is evaluated.

        Returns:
            Value of the cumulative distribution function evaluated at x.
        """
        return 1 - np.exp(-(x**2) / (2 * self.sigma**2))

    def expected_value(self) -> float:
        """Returns the expected value of the Rayleigh distribution."""
        return self.sigma * np.sqrt(np.pi / 2)

    def variance(self) -> float:
        """Returns the variance of the Rayleigh distribution."""
        return (2 - np.pi / 2) * self.sigma**2

    def rms_value(self) -> float:
        """Returns the RMS value of the Rayleigh distribution."""
        return np.sqrt(2) * self.sigma

    def get_samples(
        self, size: Union[int, Tuple[int, ...]], seed: int = None
    ) -> NDArrayFloat:
        """Generates random variables from the Rayleigh distribution.

        Args:
            size: Number of random variables to generate.
            seed: Seed for the random number generator.

        Returns:
            An array of size `size` containing random variables from the
            Rayleigh distribution.
        """
        return np.array(
            stats.rayleigh.rvs(loc=0, scale=self.sigma, size=size, random_state=seed)
        )


__all__ = ["Rayleigh"]

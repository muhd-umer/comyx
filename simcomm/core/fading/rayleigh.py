from typing import Any, Tuple, Union

import numpy as np
import numpy.typing as npt
import scipy.stats as stats


class Rayleigh:
    r"""The Rayleigh distribution is a continuous probability distribution for nonnegative-valued random variables. Up to rescaling, it coincides with the chi distribution with two degrees of freedom.

    **Density function**
        .. math::
            f(x; \sigma) = \frac{x}{\sigma^2} \cdot \exp\left(-\frac{x^2}{2\sigma^2}\right)

    **Expected value**
        .. math::
            \sigma \cdot \sqrt{\frac{\pi}{2}}

    **Variance**
        .. math::
            \left(2 - \frac{\pi}{2}\right) \cdot \sigma^2

    **RMS value**
        .. math::
            \sqrt{2} \cdot \sigma

    Attributes:
        sigma: The scale parameter of the Rayleigh distribution.

    Reference:
        https://en.wikipedia.org/wiki/Rayleigh_distribution
    """

    def __init__(self, sigma: float = 1) -> None:
        """Initializes a Rayleigh distribution with the given scale parameter.

        Args:
            sigma: The scale parameter of the Rayleigh distribution.
        """
        self.sigma = sigma

    def pdf(self, x: float) -> float:
        """Returns the probability density function of the Rayleigh distribution.

        Args:
            x: The input value.

        Returns:
            pdf: The probability density function value at x.
        """
        return (x / self.sigma**2) * np.exp(-(x**2) / (2 * self.sigma**2))

    def cdf(self, x: float) -> float:
        """Returns the cumulative distribution function of the Rayleigh distribution.

        Args:
            x: The input value.

        Returns:
            cdf: The cumulative distribution function value at x.
        """
        return 1 - np.exp(-(x**2) / (2 * self.sigma**2))

    def expected_value(self) -> float:
        """Calculates the expected value of the Rayleigh distribution.

        Returns:
            expected_value: The expected value of the Rayleigh distribution.
        """
        return self.sigma * np.sqrt(np.pi / 2)

    def variance(self) -> float:
        """Calculates the variance of the Rayleigh distribution.

        Returns:
            variance: The variance of the Rayleigh distribution.
        """
        return (2 - np.pi / 2) * self.sigma**2

    def rms_value(self) -> float:
        """Calculates the RMS value of the Rayleigh distribution.

        Returns:
            rms: The RMS value of the Rayleigh distribution.
        """
        return np.sqrt(2) * self.sigma

    def get_samples(
        self,
        size: Union[int, Tuple[int, ...]],
    ) -> npt.NDArray[np.floating[Any]]:
        """Generates random variables from the Rayleigh distribution.

        Args:
            size: The number of random variables to generate.

        Returns:
            samples: An array of size `size` containing random variables from the Rayleigh distribution.
        """
        return np.array(stats.rayleigh.rvs(loc=0, scale=self.sigma, size=size))

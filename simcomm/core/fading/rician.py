from typing import Any, Tuple, Union

import numpy as np
import numpy.typing as npt
import scipy.stats as stats
from scipy.special import i0

from ...utils import laguerre


class Rician:
    r"""The Rician distribution is a continuous probability distribution that describes the length of a two-dimensional vector with components that are independent Gaussian random variables.

    Density Function
        .. math::
            f(x) = \frac{x}{\sigma^2} \exp\left(-\frac{x^2 + \nu^2}{2\sigma^2}\right) I_0\left(\frac{x\nu}{\sigma^2}\right)

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

    Attributes:
        K (float): The Rician factor, which is the ratio between the power of the direct path and the power of the scattered paths.
        omega (float): The scale parameter, which is the total power from both the line-of-sight and scattered paths.
        sigma (float): The scale parameter, which is the standard deviation of the distribution.
        nu (float): The location parameter, which is the shift of the distribution.

    Reference:
        https://en.wikipedia.org/wiki/Rice_distribution
    """

    def __init__(self, K: float, sigma: float = 1) -> None:
        """Initialize the Rician distribution with the given parameters.

        Args:
            K (float): Rician factor := ratio between the power of direct path and the power of scattered paths.
            sigma (float): The scale parameter, which is the standard deviation of the distribution.
        """
        self.K = K
        self.sigma = sigma
        self.omega = (2 * self.K + 2) * self.sigma**2
        self.nu = np.sqrt((K / (1 + K)) * self.omega)

    def pdf(self, x: float) -> float:
        """Return the probability density function of the Rician distribution.

        Args:
            x (float): The value at which to evaluate the probability density function.

        Returns:
            pdf (float): The probability density function evaluated at x.
        """
        return (
            (x / self.sigma**2)
            * np.exp(-(x**2 + self.nu**2) / (2 * self.sigma**2))
            * i0(x * self.nu / self.sigma**2)
        )

    def cdf(self, x: float) -> npt.NDArray[np.floating[Any]]:
        """Return the cumulative distribution function of the Rician distribution.

        Args:
            x (float): The value at which to evaluate the cumulative distribution

        Returns:
            cdf (ndarray): The cumulative distribution function evaluated at x.
        """
        return stats.rice.cdf(x, self.nu / self.sigma)

    def expected_value(self) -> float:
        """Return the expected value of the Rician distribution.

        Returns:
            expected_value (float): The expected value of the Rician distribution.
        """
        arg = -self.nu**2 / (2 * self.sigma**2)
        return self.sigma * np.sqrt(np.pi / 2) * laguerre(arg, 1 / 2)

    def variance(self) -> float:
        """Return the variance of the Rician distribution.

        Returns:
            variance (float): The variance of the Rician distribution.
        """
        arg = -self.nu**2 / (2 * self.sigma**2)
        return (
            2 * self.sigma**2
            + self.nu**2
            - ((np.pi * self.sigma**2 / 2) * (laguerre(arg, 1 / 2) ** 2))
        )

    def rms_value(self) -> float:
        """Return the RMS value of the Rician distribution.

        Returns:
            rms (float): The RMS value of the Rician distribution.
        """
        return self.sigma * np.sqrt(2 + np.pi / 2)

    def get_samples(
        self, size: Union[int, Tuple[int, ...]]
    ) -> npt.NDArray[np.floating[Any]]:
        """Generate random variables from the Rician distribution.

        Args:
            size (int or tuple of ints): The number of random variables to generate.

        Returns:
            samples (array_like): An array of size `size` containing random variables from
            the Rician distribution.
        """
        return np.array(
            stats.rice.rvs(self.nu / self.sigma, scale=self.sigma, size=size)
        )

    def get_coefficients(
        self, size: Union[int, Tuple[int, ...]]
    ) -> npt.NDArray[np.complexfloating[Any, Any]]:
        """Generate complex fading coefficients from the Rician distribution.

        Args:
            size (int or tuple of ints): The number of channel coefficients to generate.

        Returns:
            coefficients (array_like): An array of size `size` containing complex channel
            coefficients from the Rician distribution.
        """
        mu = np.sqrt(self.K / (2 * (self.K + 1)))
        sigma = np.sqrt(1 / (2 * (self.K + 1)))

        # Generate the channel
        return np.array(
            (sigma * stats.norm.rvs(size=size) + mu)
            + 1j * (sigma * stats.norm.rvs(size=size) + mu)
        )

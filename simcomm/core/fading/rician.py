from typing import List, Tuple

import numpy as np
import scipy.stats as stats

from ...utils import i0, laguerre


class Rician:
    """A class representing a Rician distribution.

    Properties:
        Density function := f(x) = (x / sigma^2) * exp(-(x^2 + nu^2) / (2 * sigma^2)) * I_0(x * nu / sigma^2)
        Expected value := sigma * sqrt(pi / 2) * exp(-nu^2 / (2 * sigma^2))
        Variance := 2 * sigma^2 + nu^2 - pi * sigma^2 / 2
        RMS value := sigma * sqrt(2 + pi / 2)

    Attributes:
        K: float
            The Rician factor, which is the ratio between the power of the direct path and the power of the scattered paths.
        omega: float
            The scale parameter, which is the total power from both the line-of-sight and scattered paths.
        sigma: float
            The scale parameter, which is the standard deviation of the distribution.
        nu: float
            The location parameter, which is the shift of the distribution.

        Specify either omega or sigma, and the other will be calculated automatically.

    Reference:
        https://en.wikipedia.org/wiki/Rice_distribution
    """

    def __init__(self, K: float, sigma: float = 1) -> None:
        """Initialize the Rician distribution with the given parameters.

        Args:
            K: float
                Rician factor := ratio between the power of direct path and the power of scattered paths.
            sigma: float
                The scale parameter, which is the standard deviation of the distribution.
        """
        self.K = K
        self.sigma = sigma
        self.omega = (2 * self.K + 2) * self.sigma**2
        self.nu = np.sqrt((K / (1 + K)) * self.omega)

    def pdf(self, x: float) -> float:
        """Return the probability density function of the Rician distribution.

        Args:
            x: float
                The value at which to evaluate the probability density function.

        Returns:
            float: The probability density function evaluated at x.
        """
        return (
            (x / self.sigma**2)
            * np.exp(-(x**2 + self.nu**2) / (2 * self.sigma**2))
            * i0(x * self.nu / self.sigma**2)
        )

    def cdf(self, x: float) -> float:
        """Return the cumulative distribution function of the Rician distribution.

        Args:
            x: float
                The value at which to evaluate the cumulative distribution function.

        Returns:
            float: The cumulative distribution function evaluated at x.
        """
        return stats.rice.cdf(x, self.nu / self.sigma)

    def expected_value(self) -> float:
        """Return the expected value of the Rician distribution.

        Returns:
            float: The expected value of the Rician distribution.
        """
        arg = -self.nu**2 / (2 * self.sigma**2)
        return self.sigma * np.sqrt(np.pi / 2) * laguerre(arg, 1 / 2)

    def variance(self) -> float:
        """Return the variance of the Rician distribution.

        Returns:
            float: The variance of the Rician distribution.
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
            float: The RMS value of the Rician distribution.
        """
        return self.sigma * np.sqrt(2 + np.pi / 2)

    def generate(self, size: int) -> np.ndarray:
        """Generate random variables from the Rician distribution.

        Args:
            size: int
                The number of random variables to generate.

        Returns:
            np.ndarray: An array of random variables generated from the Rician distribution.
        """
        return stats.rice.rvs(self.nu / self.sigma, scale=self.sigma, size=size)

    def generate_coefficients(self, size: int) -> np.ndarray:
        """Generate complex fading coefficients from the Rician distribution.

        Args:
            size: int
                The number of complex fading coefficients to generate.

        Returns:
            np.ndarray: An array of complex fading coefficients generated from the Rician distribution.
        """
        mu = np.sqrt(self.K / (2 * (self.K + 1)))
        sigma = np.sqrt(1 / (2 * (self.K + 1)))

        # Generate the channel
        return (sigma * stats.norm.rvs(size=size) + mu) + 1j * (
            sigma * stats.norm.rvs(size=size) + mu
        )

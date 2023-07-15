"""
Implementation of Rician fading channel.
"""

import numpy as np
import scipy.stats as stats

from ...utils import i0, laguerre


class Rician:
    """
    A class representing a Rician distribution.

    Properties
    - Density function := f(x) = (x / sigma^2) * exp(-(x^2 + nu^2) / (2 * sigma^2)) * I_0(x * nu / sigma^2)
    - Expected value := sigma * sqrt(pi / 2) * exp(-nu^2 / (2 * sigma^2))
    - Variance := 2 * sigma^2 + nu^2 - pi * sigma^2 / 2
    - RMS value := sigma * sqrt(2 + pi / 2)

    Attributes:
        K (float): The Rician factor, which is the ratio between the power of the direct path and the power of the scattered paths.
        omega (float): The scale parameter, which is the total power from both the line-of-sight and scattered paths.
        sigma (float): The scale parameter, which is the standard deviation of the distribution.
        nu (float): The location parameter, which is the shift of the distribution.

        Specify either omega or sigma, and the other will be calculated automatically.

    Reference:
        https://en.wikipedia.org/wiki/Rice_distribution
    """

    def __init__(self, K, param, is_omega=False):
        """
        Initialize the Rician distribution with the given parameters.

        Args:
            K: Rician factor := ratio between the power of direct path and the power of scattered paths.
            param: Scale parameter := either omega or sigma depending on the value of is_omega.
            is_omega: bool := True if param is omega, False if param is sigma.
        """
        self.K = K
        if is_omega:
            self.omega = param
            self.sigma = np.sqrt(self.omega / (2 * self.K + 2))
        else:
            self.sigma = param
            self.omega = (2 * self.K + 2) * self.sigma**2
        self.nu = np.sqrt((K / (1 + K)) * self.omega)

    def pdf(self, x):
        """
        Return the probability density function of the Rician distribution.
        """
        return (
            (x / self.sigma**2)
            * np.exp(-(x**2 + self.nu**2) / (2 * self.sigma**2))
            * i0(x * self.nu / self.sigma**2)
        )

    def cdf(self, x):
        """
        Return the cumulative distribution function of the Rician distribution.
        """
        return stats.rice.cdf(x, self.nu / self.sigma)

    def expected_value(self):
        """
        Return the expected value of the Rician distribution.
        """
        arg = -self.nu**2 / (2 * self.sigma**2)
        return self.sigma * np.sqrt(np.pi / 2) * laguerre(arg, 1 / 2)

    def variance(self):
        """
        Return the variance of the Rician distribution.
        """
        arg = -self.nu**2 / (2 * self.sigma**2)
        return (
            2 * self.sigma**2
            + self.nu**2
            - ((np.pi * self.sigma**2 / 2) * (laguerre(arg, 1 / 2) ** 2))
        )

    def rms_value(self):
        """
        Return the RMS value of the Rician distribution.
        """
        return self.sigma * np.sqrt(2 + np.pi / 2)

    def generate(self, size):
        """
        Generate random variables from the Rician distribution.
        """
        return stats.rice.rvs(self.nu / self.sigma, scale=self.sigma, size=size)

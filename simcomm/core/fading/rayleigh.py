"""
Implementation of Rayleigh fading channel.
"""

import numpy as np
import scipy.stats as stats


class Rayleigh:
    """
    A class representing a Rayleigh distribution.

    Properties
    - Density function := f(x) = (x / sigma^2) * exp(-x^2 / (2 * sigma^2))
    - Expected value := sigma * sqrt(pi / 2)
    - Variance := (2 - pi / 2) * sigma^2
    - RMS value := sqrt(2) * sigma

    Attributes:
        sigma: The scale parameter of the Rayleigh distribution.

    Reference:
        https://en.wikipedia.org/wiki/Rayleigh_distribution
    """

    def __init__(self, sigma):
        self.sigma = sigma

    def pdf(self, x):
        """
        Return the probability density function of the Rayleigh distribution.
        """
        return (x / self.sigma**2) * np.exp(-(x**2) / (2 * self.sigma**2))

    def cdf(self, x):
        """
        Return the cumulative distribution function of the Rayleigh distribution.
        """
        return 1 - np.exp(-(x**2) / (2 * self.sigma**2))

    def expected_value(self):
        """
        Return the expected value of the Rayleigh distribution.
        """
        return self.sigma * np.sqrt(np.pi / 2)

    def variance(self):
        """
        Return the variance of the Rayleigh distribution.
        """
        return (2 - np.pi / 2) * self.sigma**2

    def rms_value(self):
        """
        Return the RMS value of the Rayleigh distribution.
        """
        return np.sqrt(2) * self.sigma

    def generate(self, size):
        """
        Generate random variables from the Rayleigh distribution.
        """
        return stats.rayleigh.rvs(loc=0, scale=self.sigma, size=size)

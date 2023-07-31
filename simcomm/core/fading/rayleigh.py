from typing import Any, Tuple, Union

import numpy as np
import numpy.typing as npt
import scipy.stats as stats


class Rayleigh:
    """Generates a Rayleigh fading coefficient as a complex Gaussian
    random variable with zero mean and unit variance. A class representing a Rayleigh
    distribution.

    Properties:
        - Density function := f(x) = (x / sigma^2) * exp(-x^2 / (2 * sigma^2))
        - Expected value := sigma * sqrt(pi / 2) - Variance := (2 - pi / 2) * sigma^2
        - RMS value := sqrt(2) * sigma

    Returns:
        A NumPy array of complex numbers representing the fading coefficients.

    Attributes:
        sigma (float): The scale parameter of the Rayleigh distribution.

    Reference:
        https://en.wikipedia.org/wiki/Rayleigh_distribution
    """

    def __init__(self, sigma: float = 1) -> None:
        """Initializes a Rayleigh distribution with the given scale parameter.

        Args:
            sigma (float): The scale parameter of the Rayleigh distribution.
        """
        self.sigma = sigma

    def pdf(self, x: float) -> float:
        """Returns the probability density function of the Rayleigh distribution.

        Args:
            x (float): The input value.

        Returns:
            pdf (float): The probability density function value at x.
        """
        return (x / self.sigma**2) * np.exp(-(x**2) / (2 * self.sigma**2))

    def cdf(self, x: float) -> float:
        """Returns the cumulative distribution function of the Rayleigh distribution.

        Args:
            x (float): The input value.

        Returns:
            cdf (float): The cumulative distribution function value at x.
        """
        return 1 - np.exp(-(x**2) / (2 * self.sigma**2))

    def expected_value(self) -> float:
        """Calculates the expected value of the Rayleigh distribution.

        Returns:
            expected_value (float): The expected value of the Rayleigh distribution.
        """
        return self.sigma * np.sqrt(np.pi / 2)

    def variance(self) -> float:
        """Calculates the variance of the Rayleigh distribution.

        Returns:
            variance (float): The variance of the Rayleigh distribution.
        """
        return (2 - np.pi / 2) * self.sigma**2

    def rms_value(self) -> float:
        """Calculates the RMS value of the Rayleigh distribution.

        Returns:
            rms (float): The RMS value of the Rayleigh distribution.
        """
        return np.sqrt(2) * self.sigma

    def generate_samples(
        self,
        size: Union[int, Tuple[int, ...]],
    ) -> npt.ArrayLike:
        """Generates random variables from the Rayleigh distribution.

        Args:
            size (int or tuple of ints): The number of random variables to generate.

        Returns:
            samples (array_like): An array of size `size` containing random variables from
            the Rayleigh distribution.
        """
        return stats.rayleigh.rvs(loc=0, scale=self.sigma, size=size)

    def generate_coefficients(self, size: Union[int, Tuple[int, ...]]) -> npt.ArrayLike:
        """Generates complex channel coefficients from the Rayleigh distribution.

        Args:
            size (int or tuple of ints): The number of channel coefficients to generate.

        Returns:
            coefficients (array_like): An array of size `size` containing complex channel
            coefficients from the Rayleigh distribution.
        """
        return stats.norm.rvs(scale=self.sigma, size=size) + 1j * stats.norm.rvs(
            scale=self.sigma, size=size
        )

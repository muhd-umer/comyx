import numpy as np
import scipy.stats as stats


class Rayleigh:
    """A class representing a Rayleigh distribution.

    Attributes:
        sigma: The scale parameter of the Rayleigh distribution.
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
            The probability density function value at x.
        """
        return (x / self.sigma**2) * np.exp(-(x**2) / (2 * self.sigma**2))

    def cdf(self, x: float) -> float:
        """Returns the cumulative distribution function of the Rayleigh distribution.

        Args:
            x: The input value.

        Returns:
            The cumulative distribution function value at x.
        """
        return 1 - np.exp(-(x**2) / (2 * self.sigma**2))

    def expected_value(self) -> float:
        """Calculates the expected value of the Rayleigh distribution.

        Returns:
            float: The expected value of the Rayleigh distribution.
        """
        return self.sigma * np.sqrt(np.pi / 2)

    def variance(self) -> float:
        """Calculates the variance of the Rayleigh distribution.

        Returns:
            float: The variance of the Rayleigh distribution.
        """
        return (2 - np.pi / 2) * self.sigma**2

    def rms_value(self) -> float:
        """Calculates the RMS value of the Rayleigh distribution.

        Returns:
            float: The RMS value of the Rayleigh distribution.
        """
        return np.sqrt(2) * self.sigma

    def generate(self, size: int) -> np.ndarray:
        """Generates random variables from the Rayleigh distribution.

        Args:
            size: The number of random variables to generate.

        Returns:
            An array of size `size` containing random variables from the Rayleigh distribution.
        """
        return stats.rayleigh.rvs(loc=0, scale=self.sigma, size=size)

    def generate_coefficients(self, size: int) -> np.ndarray:
        """Generates complex channel coefficients from the Rayleigh distribution.

        Args:
            size: The number of channel coefficients to generate.

        Returns:
            An array of size `size` containing complex channel coefficients from the Rayleigh distribution.
        """
        return stats.norm.rvs(scale=self.sigma, size=size) + 1j * stats.norm.rvs(
            scale=self.sigma, size=size
        )

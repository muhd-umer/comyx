import unittest

import numpy as np

from simcomm.core.propagation import get_noise_power, get_pathloss


class TestGetNoisePower(unittest.TestCase):
    def test_positive_bandwidth(self):
        """Test that positive bandwidth returns a finite value."""
        result = get_noise_power(1e6)
        self.assertTrue(np.isfinite(result))

    def test_negative_bandwidth(self):
        """Test that negative bandwidth raises a ValueError."""
        with self.assertRaises(ValueError):
            get_noise_power(-1e6)

    def test_positive_temperature(self):
        """Test that positive temperature returns a finite value."""
        result = get_noise_power(1e6, temperature=300)
        self.assertTrue(np.isfinite(result))

    def test_negative_temperature(self):
        """Test that negative temperature raises a ValueError."""
        with self.assertRaises(ValueError):
            get_noise_power(1e6, temperature=-300)

    def test_zero_noise_figure(self):
        """Test that zero noise figure returns the same value as no noise figure."""
        result1 = get_noise_power(1e6, noise_figure=0)
        result2 = get_noise_power(1e6)
        self.assertEqual(result1, result2)


class TestGetPathloss(unittest.TestCase):
    # Can ignore the rest of the types as they are implemented through formulae
    def test_invalid_type(self):
        """Test that an invalid path loss model raises a NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            get_pathloss("invalid-type", 1e3, 1e9)


if __name__ == "__main__":
    unittest.main()

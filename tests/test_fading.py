from unittest import TestCase, main

import numpy as np

from comyx.fading import get_rvs


class TestGetRvs(TestCase):
    def test_rayleigh(self):
        # Test Rayleigh distribution with a single random variable
        result = np.abs(get_rvs(1, "rayleigh", sigma=1))
        self.assertEqual(result.shape, (1,))
        self.assertGreaterEqual(result[0], 0)

        # Test Rayleigh distribution with multiple random variables
        result = np.abs(get_rvs(5, "rayleigh", sigma=1))
        self.assertEqual(result.shape, (5,))
        self.assertTrue(np.all(result >= 0))

    def test_rician(self):
        # Test Rician distribution with a single random variable
        result = np.abs(get_rvs(1, "rician", K=0, sigma=1))
        self.assertEqual(result.shape, (1,))
        self.assertGreaterEqual(result[0], 0)

        # Test Rician distribution with multiple random variables
        result = np.abs(get_rvs(5, "rician", K=0, sigma=1))
        self.assertEqual(result.shape, (5,))
        self.assertTrue(np.all(result >= 0))

    def test_invalid_type(self):
        # Test with an invalid distribution type
        with self.assertRaises(NotImplementedError):
            get_rvs(1, "invalid_type", sigma=1)


if __name__ == "__main__":
    main()

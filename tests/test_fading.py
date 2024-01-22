from unittest import TestCase, main

import numpy as np

from comyx.fading import get_rvs


class TestGetRvs(TestCase):
    def test_rayleigh(self):
        # Test Rayleigh distribution with a single random variable
        result = get_rvs("rayleigh", 1, sigma=1)
        self.assertEqual(result.shape, (1,))
        self.assertGreaterEqual(result[0], 0)

        # Test Rayleigh distribution with multiple random variables
        result = get_rvs("rayleigh", 5, sigma=1)
        self.assertEqual(result.shape, (5,))
        self.assertTrue(np.all(result >= 0))

    def test_rician(self):
        # Test Rician distribution with a single random variable
        result = get_rvs("rician", 1, K=0, sigma=1)
        self.assertEqual(result.shape, (1,))
        self.assertGreaterEqual(result[0], 0)

        # Test Rician distribution with multiple random variables
        result = get_rvs("rician", 5, K=0, sigma=1)
        self.assertEqual(result.shape, (5,))
        self.assertTrue(np.all(result >= 0))

    def test_invalid_type(self):
        # Test with an invalid distribution type
        with self.assertRaises(NotImplementedError):
            get_rvs("invalid_type", 1, sigma=1)


if __name__ == "__main__":
    main()

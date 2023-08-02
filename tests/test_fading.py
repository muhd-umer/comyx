from unittest import TestCase, main

import numpy as np

from simcomm.core.fading import get_rvs


class TestGetRvs(TestCase):
    def test_rayleigh(self):
        # Test generating 1 coefficient
        result = get_rvs("rayleigh", 1, sigma=1)
        self.assertEqual(result.shape, (1,))
        self.assertGreaterEqual(result[0], 0)

        # Test generating 5 coefficients
        result = get_rvs("rayleigh", 5, sigma=1)
        self.assertEqual(result.shape, (5,))
        self.assertTrue(np.all(result >= 0))

    def test_rician(self):
        # Test generating 1 coefficient
        result = get_rvs("rician", 1, K=0, sigma=1)
        self.assertEqual(result.shape, (1,))
        self.assertGreaterEqual(result[0], 0)

        # Test generating 5 coefficients
        result = get_rvs("rician", 5, K=0, sigma=1)
        self.assertEqual(result.shape, (5,))
        self.assertTrue(np.all(result >= 0))

    def test_invalid_type(self):
        # Test generating with invalid type
        with self.assertRaises(NotImplementedError):
            get_rvs("invalid_type", 1, sigma=1)


if __name__ == "__main__":
    main()

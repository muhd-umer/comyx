import unittest

import numpy as np

from simcomm.utils import (
    db2pow,
    dbm2pow,
    get_distance,
    inverse_qfunc,
    laguerre,
    pow2db,
    pow2dbm,
    qfunc,
    wrapTo2Pi,
)


class TestUtils(unittest.TestCase):
    def test_db2pow(self):
        self.assertEqual(db2pow(0), 1)
        self.assertEqual(db2pow(10), 10)
        self.assertEqual(db2pow(-10), 0.1)
        self.assertTrue(
            np.allclose(db2pow(np.array([0, 10, -10])), np.array([1, 10, 0.1]))
        )

    def test_pow2db(self):
        self.assertEqual(pow2db(1), 0)
        self.assertEqual(pow2db(10), 10)
        self.assertEqual(pow2db(0.1), -10)
        self.assertTrue(
            np.allclose(pow2db(np.array([1, 10, 0.1])), np.array([0, 10, -10]))
        )

    def test_dbm2pow(self):
        self.assertEqual(dbm2pow(0), 1e-3)
        self.assertEqual(dbm2pow(10), 1e-2)
        self.assertEqual(dbm2pow(-10), 1e-4)
        self.assertTrue(
            np.allclose(dbm2pow(np.array([0, 10, -10])), np.array([1e-3, 1e-2, 1e-4]))
        )

    def test_pow2dbm(self):
        self.assertEqual(pow2dbm(1e-3), 0)
        self.assertEqual(pow2dbm(1e-2), 10)
        self.assertEqual(pow2dbm(1e-4), -10)
        self.assertTrue(
            np.allclose(pow2dbm(np.array([1e-3, 1e-2, 1e-4])), np.array([0, 10, -10]))
        )

    def test_get_distance(self):
        self.assertEqual(get_distance([0, 0], [3, 4]), 5)
        self.assertEqual(get_distance([0, 0, 0], [3, 4, 0]), 5)
        self.assertEqual(get_distance([0, 0], [3, 4, 0]), 5)
        with self.assertRaises(ValueError):
            get_distance([0, 0], [3, 4], dim=4)

    def test_qfunc(self):
        self.assertEqual(qfunc(0), 0.5)
        self.assertEqual(qfunc(np.inf), 0)
        self.assertEqual(qfunc(-np.inf), 1)
        self.assertTrue(
            np.allclose(qfunc(np.array([0, np.inf, -np.inf])), np.array([0.5, 0, 1]))
        )

    def test_inverse_qfunc(self):
        self.assertEqual(inverse_qfunc(0.5), 0)
        self.assertEqual(inverse_qfunc(0), np.inf)
        self.assertEqual(inverse_qfunc(1), -np.inf)
        self.assertTrue(
            np.allclose(
                inverse_qfunc(np.array([0.5, 0, 1])), np.array([0, np.inf, -np.inf])
            )
        )

    def test_laguerre(self):
        self.assertEqual(laguerre(0, 0), 1)
        self.assertEqual(laguerre(0, 1), 1)
        self.assertEqual(laguerre(0, 2), 1)
        self.assertEqual(laguerre(1, 0), 1)
        self.assertEqual(laguerre(1, 1), 0)
        self.assertEqual(laguerre(1, 2), -0.5)
        self.assertTrue(np.allclose(laguerre(np.array([0, 1]), 2), np.array([1, -0.5])))

    def test_wrapTo2Pi(self):
        self.assertEqual(wrapTo2Pi(np.array(0)), 0)
        self.assertEqual(wrapTo2Pi(np.array(2 * np.pi)), 0)
        self.assertEqual(wrapTo2Pi(np.array(3 * np.pi)), np.pi)
        self.assertTrue(
            np.allclose(
                wrapTo2Pi(np.array([0, 2 * np.pi, 3 * np.pi])), np.array([0, 0, np.pi])
            )
        )


if __name__ == "__main__":
    unittest.main()

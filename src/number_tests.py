"""My experiment with unit tests, for functions in number.py that might be updated often."""
import number, gmpy2
import unittest

class IsPrimeTest(unittest.TestCase):
    """Checks is_prime over a range and for special numbers."""
    def test_special_nums(self):
        self.assertFalse(number.is_prime(-1))
        self.assertFalse(number.is_prime(0))
        self.assertFalse(number.is_prime(1))

    def test_1000(self):
        for n in range(2, 1000):
            self.assertEqual(number.is_prime(n), gmpy2.is_prime(n), msg=n)

    def test_strong_psuedoprimes(self):
        """Tests strong pseudoprimes base 2: A001262"""
        strong_psuedoprimes = (2047, 3277, 4033, 4681, 8321, 15841, 29341, 42799, 49141, 52633, 65281, 74665, 80581,
                               85489, 88357, 90751, 104653, 130561, 196093, 220729)
        for sp in strong_psuedoprimes:
            self.assertEqual(number.is_prime(sp), gmpy2.is_prime(sp), msg=sp)

    def test_deterministic_nums(self):
        """Tests special odd numbers that fail deterministic tests of first n primes: A014233"""
        terms = (2047, 1373653, 25326001, 3215031751, 2152302898747, 3474749660383, 341550071728321,
                 3825123056546413051, 318665857834031151167461, 3317044064679887385961981)
        for n in terms:
            self.assertEqual(number.is_prime(n), gmpy2.is_prime(n), msg=n)


class PhiTest(unittest.TestCase):
    """Checks Euler's totient function against known values"""
    def test_values(self):
        phi_values = (1, 1, 2, 2, 4, 2, 6, 4, 6, 4)
        for n in range(10):
            self.assertEqual(number.phi(n+1), phi_values[n], msg=n)

        self.assertEqual(number.phi(100), 40)


class IsSquareTest(unittest.TestCase):
    """Checks is_square (non floating point version) against obvious numbers"""
    def test_values(self):
        self.assertTrue(number.is_square(1))
        self.assertFalse(number.is_square(2))
        self.assertFalse(number.is_square(120))
        self.assertTrue(number.is_square(121))
        self.assertTrue(number.is_square(12345678987654321234567 ** 2))


if __name__ == "__main__":
    unittest.main(verbosity=2)
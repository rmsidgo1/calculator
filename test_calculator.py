import math
import unittest

from calculator import Calculator


class TestArithmetic(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = Calculator()

    def test_add(self) -> None:
        self.assertEqual(self.calc.add(1, 2), 3)
        self.assertEqual(self.calc.add(-1, 1), 0)

    def test_subtract(self) -> None:
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(0, 5), -5)

    def test_multiply(self) -> None:
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(-2, 3), -6)

    def test_divide(self) -> None:
        self.assertAlmostEqual(self.calc.divide(10, 4), 2.5)
        self.assertAlmostEqual(self.calc.divide(-6, 2), -3.0)

    def test_divide_by_zero(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(1, 0)

    def test_modulo(self) -> None:
        self.assertEqual(self.calc.modulo(10, 3), 1)
        self.assertEqual(self.calc.modulo(7, 7), 0)

    def test_modulo_by_zero(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            self.calc.modulo(5, 0)

    def test_power(self) -> None:
        self.assertEqual(self.calc.power(2, 10), 1024)
        self.assertAlmostEqual(self.calc.power(4, 0.5), 2.0)


class TestSqrtLog(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = Calculator()

    def test_sqrt(self) -> None:
        self.assertAlmostEqual(self.calc.sqrt(9), 3.0)
        self.assertAlmostEqual(self.calc.sqrt(2), math.sqrt(2))

    def test_sqrt_negative(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.sqrt(-1)

    def test_sqrt_zero(self) -> None:
        self.assertEqual(self.calc.sqrt(0), 0.0)

    def test_cbrt(self) -> None:
        self.assertAlmostEqual(self.calc.cbrt(8), 2.0)
        self.assertAlmostEqual(self.calc.cbrt(-27), -3.0)

    def test_log_default_base(self) -> None:
        self.assertAlmostEqual(self.calc.log(100), 2.0)
        self.assertAlmostEqual(self.calc.log(1000), 3.0)

    def test_log_custom_base(self) -> None:
        self.assertAlmostEqual(self.calc.log(8, 2), 3.0)

    def test_log_non_positive(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.log(0)
        with self.assertRaises(ValueError):
            self.calc.log(-1)

    def test_ln(self) -> None:
        self.assertAlmostEqual(self.calc.ln(math.e), 1.0)
        self.assertAlmostEqual(self.calc.ln(1), 0.0)

    def test_ln_non_positive(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.ln(0)

    def test_exp(self) -> None:
        self.assertAlmostEqual(self.calc.exp(0), 1.0)
        self.assertAlmostEqual(self.calc.exp(1), math.e)


class TestTrigonometry(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = Calculator()

    def test_sin_radians(self) -> None:
        self.assertAlmostEqual(self.calc.sin(0), 0.0)
        self.assertAlmostEqual(self.calc.sin(math.pi / 2), 1.0)

    def test_sin_degrees(self) -> None:
        self.assertAlmostEqual(self.calc.sin(90, degree=True), 1.0)
        self.assertAlmostEqual(self.calc.sin(0, degree=True), 0.0)

    def test_cos_radians(self) -> None:
        self.assertAlmostEqual(self.calc.cos(0), 1.0)
        self.assertAlmostEqual(self.calc.cos(math.pi), -1.0)

    def test_cos_degrees(self) -> None:
        self.assertAlmostEqual(self.calc.cos(180, degree=True), -1.0)

    def test_tan_radians(self) -> None:
        self.assertAlmostEqual(self.calc.tan(0), 0.0)
        self.assertAlmostEqual(self.calc.tan(math.pi / 4), 1.0)

    def test_tan_degrees(self) -> None:
        self.assertAlmostEqual(self.calc.tan(45, degree=True), 1.0)

    def test_asin_radians(self) -> None:
        self.assertAlmostEqual(self.calc.asin(1), math.pi / 2)

    def test_asin_degrees(self) -> None:
        self.assertAlmostEqual(self.calc.asin(1, degree=True), 90.0)

    def test_acos_radians(self) -> None:
        self.assertAlmostEqual(self.calc.acos(-1), math.pi)

    def test_acos_degrees(self) -> None:
        self.assertAlmostEqual(self.calc.acos(-1, degree=True), 180.0)

    def test_atan_radians(self) -> None:
        self.assertAlmostEqual(self.calc.atan(1), math.pi / 4)

    def test_atan_degrees(self) -> None:
        self.assertAlmostEqual(self.calc.atan(1, degree=True), 45.0)

    def test_atan2_radians(self) -> None:
        self.assertAlmostEqual(self.calc.atan2(1, 1), math.pi / 4)

    def test_atan2_degrees(self) -> None:
        self.assertAlmostEqual(self.calc.atan2(1, 1, degree=True), 45.0)


class TestHyperbolic(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = Calculator()

    def test_sinh(self) -> None:
        self.assertAlmostEqual(self.calc.sinh(0), 0.0)
        self.assertAlmostEqual(self.calc.sinh(1), math.sinh(1))

    def test_cosh(self) -> None:
        self.assertAlmostEqual(self.calc.cosh(0), 1.0)
        self.assertAlmostEqual(self.calc.cosh(1), math.cosh(1))

    def test_tanh(self) -> None:
        self.assertAlmostEqual(self.calc.tanh(0), 0.0)
        self.assertAlmostEqual(self.calc.tanh(1), math.tanh(1))


class TestNumberTheory(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = Calculator()

    def test_factorial(self) -> None:
        self.assertEqual(self.calc.factorial(0), 1)
        self.assertEqual(self.calc.factorial(5), 120)

    def test_factorial_negative(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.factorial(-1)

    def test_factorial_non_integer(self) -> None:
        with self.assertRaises(ValueError):
            self.calc.factorial(2.5)  # type: ignore[arg-type]

    def test_gcd(self) -> None:
        self.assertEqual(self.calc.gcd(12, 8), 4)
        self.assertEqual(self.calc.gcd(7, 5), 1)

    def test_lcm(self) -> None:
        self.assertEqual(self.calc.lcm(4, 6), 12)
        self.assertEqual(self.calc.lcm(7, 3), 21)

    def test_abs_val(self) -> None:
        self.assertEqual(self.calc.abs_val(-5), 5)
        self.assertEqual(self.calc.abs_val(3.14), 3.14)

    def test_ceil(self) -> None:
        self.assertEqual(self.calc.ceil(2.1), 3)
        self.assertEqual(self.calc.ceil(-1.9), -1)

    def test_floor(self) -> None:
        self.assertEqual(self.calc.floor(2.9), 2)
        self.assertEqual(self.calc.floor(-1.1), -2)

    def test_round_val(self) -> None:
        self.assertEqual(self.calc.round_val(2.567, 2), 2.57)
        self.assertEqual(self.calc.round_val(2.5), 2)


class TestHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = Calculator()

    def test_history_records(self) -> None:
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        hist = self.calc.history()
        self.assertEqual(len(hist), 2)
        self.assertEqual(hist[0]["result"], 3)
        self.assertEqual(hist[1]["result"], 12)

    def test_last_result(self) -> None:
        self.assertIsNone(self.calc.last_result())
        self.calc.add(1, 2)
        self.assertEqual(self.calc.last_result(), 3)

    def test_clear_history(self) -> None:
        self.calc.add(1, 2)
        self.calc.clear_history()
        self.assertEqual(self.calc.history(), [])
        self.assertIsNone(self.calc.last_result())

    def test_history_limit(self) -> None:
        calc = Calculator(history_limit=3)
        for i in range(5):
            calc.add(i, 0)
        hist = calc.history()
        self.assertEqual(len(hist), 3)
        self.assertEqual(hist[0]["result"], 2)

    def test_history_returns_copy(self) -> None:
        self.calc.add(1, 2)
        hist = self.calc.history()
        hist.append({"expression": "fake", "result": 0})
        self.assertEqual(len(self.calc.history()), 1)


if __name__ == "__main__":
    unittest.main()

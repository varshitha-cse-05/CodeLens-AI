
import unittest

from trace_engine import analyze


class TestTraceEngine(unittest.TestCase):

    def test_simple_assignment(self):
        steps = analyze("x = 5")
        self.assertEqual(steps[-1]["variables"]["x"], 5)

    def test_arithmetic(self):
        steps = analyze("x = 5\ny = x + 3\nz = y * 2")
        self.assertEqual(steps[-1]["variables"]["z"], 16)

    def test_undefined_variable(self):
        with self.assertRaisesRegex(ValueError, "Undefined variable"):
            analyze("x = missing + 1")

    def test_division_by_zero(self):
        with self.assertRaisesRegex(ValueError, "Division by zero"):
            analyze("x = 10 // 0")


if __name__ == "__main__":
    unittest.main()

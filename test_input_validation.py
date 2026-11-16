
import unittest

from input_validation import has_valid_required_measurements


class TestInputValidation(unittest.TestCase):

    def test_valid_measurements(self):
        self.assertTrue(
            has_valid_required_measurements(120, 25.0, 70)
        )

    def test_zero_glucose(self):
        self.assertFalse(
            has_valid_required_measurements(0, 25.0, 70)
        )

    def test_zero_bmi(self):
        self.assertFalse(
            has_valid_required_measurements(120, 0, 70)
        )

    def test_zero_blood_pressure(self):
        self.assertFalse(
            has_valid_required_measurements(120, 25.0, 0)
        )


if __name__ == "__main__":
    unittest.main()

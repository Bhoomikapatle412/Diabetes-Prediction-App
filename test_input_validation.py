
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

    def test_negative_glucose(self):
        self.assertFalse(
            has_valid_required_measurements(-10, 25.0, 70)
        )

    def test_negative_bmi(self):
        self.assertFalse(
            has_valid_required_measurements(120, -5.0, 70)
        )

    def test_none_value(self):
        self.assertFalse(
            has_valid_required_measurements(None, 25.0, 70)
        )

    def test_non_numeric_glucose(self):
        self.assertFalse(
            has_valid_required_measurements("abc", 25.0, 70)
        )

    def test_string_numeric_values(self):
        self.assertTrue(
            has_valid_required_measurements("120", "25.0", "70")
        )

    def test_invalid_blood_pressure(self):
        self.assertFalse(
            has_valid_required_measurements(120, 25.0, "abc")
        )
        
    def test_nan_glucose(self):
        self.assertFalse(
            has_valid_required_measurements(float("nan"), 25.0, 70)
        )

    def test_infinite_bmi(self):
        self.assertFalse(
            has_valid_required_measurements(120, float("inf"), 70)
        )

    def test_negative_infinity_blood_pressure(self):
        self.assertFalse(
            has_valid_required_measurements(120, 25.0, float("-inf"))
        )

if __name__ == "__main__":
    unittest.main()

import math


def has_valid_required_measurements(glucose, bmi, blood_pressure):
    """
    Validate required health measurements.
    Reject missing, non-numeric, non-finite, zero and negative values.
    """
    try:
        values = [glucose, bmi, blood_pressure]

        return all(
            value is not None
            and math.isfinite(float(value))
            and float(value) > 0
            for value in values
        )

    except (ValueError, TypeError):
        return False
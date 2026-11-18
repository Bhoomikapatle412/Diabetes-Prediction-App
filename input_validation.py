
def has_valid_required_measurements(glucose, bmi, blood_pressure):
    """
    Validate required health measurements.
    """
    try:
        values = [glucose, bmi, blood_pressure]

        return all(
            value is not None
            and float(value) > 0
            for value in values
        )

    except (ValueError, TypeError):
        return False

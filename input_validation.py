def has_valid_required_measurements(glucose, bmi, blood_pressure):
    """
    Check whether required health measurements are non-zero.
    """
    return glucose > 0 and bmi > 0 and blood_pressure > 0

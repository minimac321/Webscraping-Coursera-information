import logging

from src.constants import APPLICATION_NAME


def get_logger():
    logger = logging.getLogger(APPLICATION_NAME)
    logger_handler = logging.StreamHandler()
    logger.addHandler(logger_handler)
    logger.setLevel(logging.INFO)
    return logger


def value_to_float(value) -> float:
    """
    Convert a value which may be a string, float or int to a float.
    """
    if type(value) == float or type(value) == int:
        return value

    value = value.replace(",", ".").upper()
    if "K" in value:
        if len(value) > 1:
            return float(value.replace("K", "")) * 1000
        return 1000.0
    if "M" in value:
        if len(value) > 1:
            return float(value.replace("M", "")) * 1000000
        return 1000000.0
    if "B" in value:
        return float(value.replace("B", "")) * 1000000000

    return 0.0

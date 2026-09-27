class CircuitCalculationError(Exception):
    """Base exception for all circuit-related errors."""

    pass


class InvalidParameterError(CircuitCalculationError):
    """Raised when provided parameters are invalid (e.g. negative values)."""

    pass


class MissingParameterError(CircuitCalculationError):
    """Raised when required parameters are missing for a formula."""

    pass

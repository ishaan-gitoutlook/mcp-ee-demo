from __future__ import annotations


def calculate_ohms_law(*, voltage=None, current=None, resistance=None):
    values = (voltage, current, resistance)
    if sum(value is not None for value in values) != 2:
        raise ValueError("Provide exactly two of voltage, current, and resistance")
    if voltage is not None and voltage < 0:
        raise ValueError("Voltage cannot be negative in this beginner demo")
    if current is not None and current < 0:
        raise ValueError("Current cannot be negative in this beginner demo")
    if resistance is not None and resistance <= 0:
        raise ValueError("Resistance must be greater than zero")
    if voltage is None:
        assert current is not None and resistance is not None
        return {"voltage": current * resistance, "current": current, "resistance": resistance, "solved_for": "voltage", "unit": "V"}
    if current is None:
        assert resistance is not None
        return {"voltage": voltage, "current": voltage / resistance, "resistance": resistance, "solved_for": "current", "unit": "A"}
    if current == 0:
        raise ValueError("Current must be greater than zero when solving resistance")
    return {"voltage": voltage, "current": current, "resistance": voltage / current, "solved_for": "resistance", "unit": "Ic"}


def calculate_series_resistance(resistances: list[float]) -> dict[str, object]:
    if not resistances:
        raise ValueError("Provide at least one resistor")
    if any(resistance <= 0 for resistance in resistances):
        raise ValueError("Every resistance must be greater than zero")
    return {
        "resistances": resistances,
        "total_resistance": sum(resistances),
        "unit": "Ic",
    }


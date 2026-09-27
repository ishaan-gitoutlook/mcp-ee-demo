from typing import TypedDict

from ee_mcp_demo.core.exceptions import InvalidParameterError, MissingParameterError


class OhmsLawResult(TypedDict):
    voltage: float
    current: float
    resistance: float
    solved_for: str
    unit: str


class SeriesResistanceResult(TypedDict):
    resistances: list[float]
    total_resistance: float
    unit: str


class ParallelResistanceResult(TypedDict):
    resistances: list[float]
    total_resistance: float
    unit: str


class PowerResult(TypedDict):
    voltage: float
    current: float
    power: float
    unit: str


class CoulombsLawResult(TypedDict):
    charge_1: float
    charge_2: float
    distance: float
    force: float
    unit: str


class ChargeResult(TypedDict):
    capacitance: float
    voltage: float
    charge: float
    unit: str


def calculate_ohms_law(
    *,
    voltage: float | None = None,
    current: float | None = None,
    resistance: float | None = None,
) -> OhmsLawResult:
    """Calculates the missing value in Ohm's Law (V = I * R)."""
    values = (voltage, current, resistance)

    if sum(value is not None for value in values) != 2:
        raise MissingParameterError("Provide exactly two of voltage, current, and resistance")

    if voltage is not None and voltage < 0:
        raise InvalidParameterError("Voltage cannot be negative in this beginner demo")
    if current is not None and current < 0:
        raise InvalidParameterError("Current cannot be negative in this beginner demo")
    if resistance is not None and resistance <= 0:
        raise InvalidParameterError("Resistance must be greater than zero")

    if voltage is None:
        assert current is not None and resistance is not None
        return {
            "voltage": current * resistance,
            "current": current,
            "resistance": resistance,
            "solved_for": "voltage",
            "unit": "V",
        }

    if current is None:
        assert resistance is not None
        return {
            "voltage": voltage,
            "current": voltage / resistance,
            "resistance": resistance,
            "solved_for": "current",
            "unit": "A",
        }

    if current == 0:
        raise InvalidParameterError("Current must be greater than zero when solving resistance")
    return {
        "voltage": voltage,
        "current": current,
        "resistance": voltage / current,
        "solved_for": "resistance",
        "unit": "Ω",
    }


def calculate_series_resistance(resistances: list[float]) -> SeriesResistanceResult:
    """Adds up a list of resistors in series."""
    if not resistances:
        raise MissingParameterError("Provide at least one resistor")
    if any(resistance <= 0 for resistance in resistances):
        raise InvalidParameterError("Every resistance must be greater than zero")

    return {
        "resistances": resistances,
        "total_resistance": sum(resistances),
        "unit": "Ω",
    }


def calculate_parallel_resistance(resistances: list[float]) -> ParallelResistanceResult:
    """Calculates total resistance for resistors in parallel."""
    if not resistances:
        raise MissingParameterError("Provide at least one resistor")
    if any(resistance <= 0 for resistance in resistances):
        raise InvalidParameterError("Every resistance must be greater than zero")

    inverse_sum = sum(1.0 / r for r in resistances)
    total_resistance = 1.0 / inverse_sum

    return {
        "resistances": resistances,
        "total_resistance": total_resistance,
        "unit": "Ω",
    }


def calculate_electrical_power(
    *, voltage: float | None = None, current: float | None = None
) -> PowerResult:
    """Calculates electrical power given Voltage and Current (P = V * I)."""
    if voltage is None or current is None:
        raise MissingParameterError(
            "Both voltage and current are required to calculate power in this demo"
        )

    return {
        "voltage": voltage,
        "current": current,
        "power": voltage * current,
        "unit": "W",
    }


def calculate_coulombs_law(q1: float, q2: float, r: float) -> CoulombsLawResult:
    """Calculates electrostatic force using Coulomb's Law."""
    if r <= 0:
        raise InvalidParameterError("Distance must be greater than zero")

    k = 8.9875517923e9
    force = k * (q1 * q2) / (r * r)

    return {
        "charge_1": q1,
        "charge_2": q2,
        "distance": r,
        "force": force,
        "unit": "N",
    }


def calculate_charge(capacitance: float, voltage: float) -> ChargeResult:
    """Calculates stored charge in a capacitor (Q = C * V)."""
    if capacitance < 0:
        raise InvalidParameterError("Capacitance cannot be negative")

    return {
        "capacitance": capacitance,
        "voltage": voltage,
        "charge": capacitance * voltage,
        "unit": "C",
    }

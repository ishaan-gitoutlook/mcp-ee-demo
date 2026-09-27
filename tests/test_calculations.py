import pytest

from ee_mcp_demo.core.calculations import (
    calculate_charge,
    calculate_coulombs_law,
    calculate_electrical_power,
    calculate_ohms_law,
    calculate_parallel_resistance,
    calculate_series_resistance,
)
from ee_mcp_demo.core.exceptions import InvalidParameterError, MissingParameterError


def test_calculates_current_from_voltage_and_resistance() -> None:
    assert calculate_ohms_law(voltage=12, resistance=6) == {
        "voltage": 12,
        "current": 2,
        "resistance": 6,
        "solved_for": "current",
        "unit": "A",
    }


def test_requires_exactly_two_values() -> None:
    with pytest.raises(MissingParameterError, match="exactly two"):
        calculate_ohms_law(voltage=12)


def test_rejects_zero_resistance() -> None:
    with pytest.raises(InvalidParameterError, match="greater than zero"):
        calculate_ohms_law(current=2, resistance=0)


def test_adds_series_resistors() -> None:
    assert calculate_series_resistance([100, 220, 330]) == {
        "resistances": [100, 220, 330],
        "total_resistance": 650,
        "unit": "Ω",
    }


def test_rejects_empty_or_non_positive_resistors() -> None:
    with pytest.raises(MissingParameterError, match="at least one"):
        calculate_series_resistance([])
    with pytest.raises(InvalidParameterError, match="greater than zero"):
        calculate_series_resistance([100, 0])


def test_adds_parallel_resistors() -> None:
    result = calculate_parallel_resistance([100, 100])
    assert result["total_resistance"] == 50.0
    assert result["unit"] == "Ω"


def test_calculates_electrical_power() -> None:
    result = calculate_electrical_power(voltage=12, current=2)
    assert result["power"] == 24
    assert result["unit"] == "W"




def test_calculates_coulombs_law() -> None:
    result = calculate_coulombs_law(1e-6, 1e-6, 1.0)
    assert round(result["force"], 4) == 0.0090
    assert result["unit"] == "N"


def test_calculates_charge() -> None:
    result = calculate_charge(0.001, 5)
    assert result["charge"] == 0.005
    assert result["unit"] == "C"

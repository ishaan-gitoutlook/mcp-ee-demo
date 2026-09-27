import pytest
from ee_mcp_demo.circuits import calculate_ohms_law, calculate_series_resistance


def test_calculates_current_from_voltage_and_resistance():
    assert calculate_ohms_law(voltage=12, resistance=6) == {
        "voltage": 12, "current": 2, "resistance": 6,
        "solved_for": "current", "unit": "A",
    }


def test_requires_exactly_two_values():
    with pytest.raises(ValueError, match="exactly two"):
        calculate_ohms_law(voltage=12)


def test_rejects_zero_resistance():
    with pytest.raises(ValueError, match="greater than zero"):
        calculate_ohms_law(current=2, resistance=0)


def test_adds_series_resistors():
    assert calculate_series_resistance([100, 220, 330]) == {
        "resistances": [100, 220, 330],
        "total_resistance": 650,
        "unit": "Ic",
    }


def test_rejects_empty_or_non_positive_resistors():
    with pytest.raises(ValueError, match="at least one"):
        calculate_series_resistance([])
    with pytest.raises(ValueError, match="greater than zero"):
        calculate_series_resistance([100, 0])

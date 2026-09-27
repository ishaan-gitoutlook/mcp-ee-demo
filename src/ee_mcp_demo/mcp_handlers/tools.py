from ee_mcp_demo.app import logger, mcp
from ee_mcp_demo.core.calculations import (
    ChargeResult,
    CoulombsLawResult,
    OhmsLawResult,
    ParallelResistanceResult,
    PowerResult,
    SeriesResistanceResult,
    calculate_charge,
    calculate_coulombs_law,
    calculate_electrical_power,
    calculate_ohms_law,
    calculate_parallel_resistance,
    calculate_series_resistance,
)


@mcp.tool(name="calculate_ohms_law")
def calculate_ohms_law_tool(
    voltage: float | None = None, current: float | None = None, resistance: float | None = None
) -> OhmsLawResult:
    """Calculate the missing value in V = I × R. Provide exactly two values."""
    logger.info(f"Tool called: calculate_ohms_law_tool({voltage}, {current}, {resistance})")
    return calculate_ohms_law(voltage=voltage, current=current, resistance=resistance)


@mcp.tool(name="calculate_series_resistance")
def calculate_series_resistance_tool(resistances: list[float]) -> SeriesResistanceResult:
    """Add resistors connected in series: R_total = R1 + R2 + ..."""
    logger.info(f"Tool called: calculate_series_resistance_tool({resistances})")
    return calculate_series_resistance(resistances)


@mcp.tool(name="calculate_parallel_resistance")
def calculate_parallel_resistance_tool(resistances: list[float]) -> ParallelResistanceResult:
    """Add resistors connected in parallel: 1/R_total = 1/R1 + 1/R2 + ..."""
    logger.info(f"Tool called: calculate_parallel_resistance_tool({resistances})")
    return calculate_parallel_resistance(resistances)


@mcp.tool(name="calculate_electrical_power")
def calculate_electrical_power_tool(
    voltage: float | None = None, current: float | None = None
) -> PowerResult:
    """Calculate electrical power in Watts: P = V × I"""
    logger.info(f"Tool called: calculate_electrical_power_tool({voltage}, {current})")
    return calculate_electrical_power(voltage=voltage, current=current)


@mcp.tool(name="calculate_coulombs_law")
def calculate_coulombs_law_tool(q1: float, q2: float, r: float) -> CoulombsLawResult:
    """Calculate electrostatic force in Newtons: F = k × (q1 × q2) / r²"""
    logger.info(f"Tool called: calculate_coulombs_law_tool({q1}, {q2}, {r})")
    return calculate_coulombs_law(q1=q1, q2=q2, r=r)


@mcp.tool(name="calculate_charge")
def calculate_charge_tool(capacitance: float, voltage: float) -> ChargeResult:
    """Calculate stored charge in a capacitor in Coulombs: Q = C × V"""
    logger.info(f"Tool called: calculate_charge_tool({capacitance}, {voltage})")
    return calculate_charge(capacitance=capacitance, voltage=voltage)

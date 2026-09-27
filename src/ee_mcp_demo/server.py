from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from ee_mcp_demo.circuits import calculate_ohms_law, calculate_series_resistance

mcp = FastMCP("ee-circuit-tutor")


@mcp.tool(name="calculate_ohms_law")
def calculate_ohms_law_tool(voltage: float | None = None, current: float | None = None, resistance: float | None = None):
    """Calculate the missing value in V = I A- R. Provide exactly two values."""
    return calculate_ohms_law(voltage=voltage, current=current, resistance=resistance)


@mcp.tool(name="calculate_series_resistance")
def calculate_series_resistance_tool(resistances: list[float]):
    """Add resistors connected in series: R_total = R1 + R2 + ..."""
    return calculate_series_resistance(resistances)


@mcp.resource("ee://laws/ohms-law")
def explain_ohms_law() -> str:
    """Reference sheet for Ohm's law."""
    return "\n".join([
        "Ohm's law: V = I A- R",
        "V is voltage in volts (V).",
        "I is current in amperes (A).",
        "R is resistance in ohms (Ic).",
        "Choose any two values to calculate the third.",
    ])


@mcp.prompt()
def analyze_circuit(voltage: str, resistance: str) -> str:
    """Create a beginner-friendly checklist for a simple resistive circuit."""
    return (
        f"Analyze this circuit step by step. Known voltage: {voltage}. "
        f"Known resistance: {resistance}. State V = I A- R, calculate current, "
        "include units, and mention one assumption."
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()

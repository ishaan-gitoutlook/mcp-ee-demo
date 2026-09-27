from ee_mcp_demo.app import logger, mcp


@mcp.resource("ee://laws/ohms-law")
def explain_ohms_law() -> str:
    """Reference sheet for Ohm's law."""
    logger.info("Resource requested: ohms-law")
    return "\n".join(
        [
            "Ohm's law: V = I × R",
            "V is voltage in volts (V).",
            "I is current in amperes (A).",
            "R is resistance in ohms (Ω).",
            "Choose any two values to calculate the third.",
        ]
    )


@mcp.resource("ee://laws/kirchhoffs-laws")
def explain_kirchhoffs_laws() -> str:
    """Reference sheet for Kirchhoff's laws."""
    logger.info("Resource requested: kirchhoffs-laws")
    return "\n".join(
        [
            "Kirchhoff's Current Law (KCL): The total current entering a "
            "junction equals the total current leaving it.",
            "Kirchhoff's Voltage Law (KVL): The directed sum of the potential "
            "differences (voltages) around any closed loop is zero.",
            "These laws are fundamental for analyzing complex electrical circuits.",
        ]
    )


@mcp.resource("ee://laws/coulombs-law")
def explain_coulombs_law() -> str:
    """Reference sheet for Coulomb's Law."""
    logger.info("Resource requested: coulombs-law")
    return "\n".join(
        [
            "Coulomb's Law: F = k × (q1 × q2) / r²",
            "F is the electrostatic force in Newtons (N).",
            "q1 and q2 are the charges in Coulombs (C).",
            "r is the distance between the charges in meters (m).",
            "k is Coulomb's constant (~8.99 × 10^9 N m²/C²).",
        ]
    )


@mcp.resource("ee://laws/capacitance")
def explain_capacitance() -> str:
    """Reference sheet for Capacitance."""
    logger.info("Resource requested: capacitance")
    return "\n".join(
        [
            "Capacitor Charge: Q = C × V",
            "Q is the charge stored in Coulombs (C).",
            "C is the capacitance in Farads (F).",
            "V is the voltage across the capacitor in Volts (V).",
        ]
    )

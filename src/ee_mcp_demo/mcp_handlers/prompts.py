from ee_mcp_demo.app import logger, mcp


@mcp.prompt()
def analyze_circuit(voltage: str, resistance: str) -> str:
    """Create a beginner-friendly checklist for a simple resistive circuit."""
    logger.info(f"Prompt requested: analyze_circuit(V={voltage}, R={resistance})")
    return (
        f"Analyze this circuit step by step. Known voltage: {voltage}. "
        f"Known resistance: {resistance}. State V = I × R, calculate current, "
        "include units, and mention one assumption."
    )


@mcp.prompt()
def analyze_parallel_circuit(r1: str, r2: str) -> str:
    """Create a beginner-friendly checklist for two parallel resistors."""
    logger.info(f"Prompt requested: analyze_parallel_circuit(R1={r1}, R2={r2})")
    return (
        f"Analyze this parallel circuit. Known resistors: R1 = {r1}, R2 = {r2}. "
        "State the parallel resistance formula, calculate total resistance, "
        "include units, and explain why the total is less than the smallest resistor."
    )

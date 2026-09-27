from ee_mcp_demo.app import mcp
from ee_mcp_demo.mcp_handlers.prompts import (
    analyze_circuit,
    analyze_parallel_circuit,
)
from ee_mcp_demo.mcp_handlers.resources import (
    explain_kirchhoffs_laws,
    explain_ohms_law,
)
from ee_mcp_demo.mcp_handlers.tools import (
    calculate_electrical_power_tool,
    calculate_ohms_law_tool,
    calculate_parallel_resistance_tool,
    calculate_series_resistance_tool,
)


def test_server_name() -> None:
    assert mcp.name == "mcp-circuit-sandbox"


def test_tool_wrappers_return_circuit_results() -> None:
    assert calculate_ohms_law_tool(voltage=9, resistance=3)["current"] == 3
    assert calculate_series_resistance_tool(resistances=[100, 220])["total_resistance"] == 320
    assert calculate_parallel_resistance_tool(resistances=[100, 100])["total_resistance"] == 50.0
    assert calculate_electrical_power_tool(voltage=12, current=2)["power"] == 24


def test_resource_and_prompt_content() -> None:
    assert "V = I × R" in explain_ohms_law()
    assert "KCL" in explain_kirchhoffs_laws()

    prompt = analyze_circuit(voltage="12 V", resistance="6 Ω")
    assert "12 V" in prompt and "6 Ω" in prompt

    parallel_prompt = analyze_parallel_circuit(r1="10 Ω", r2="20 Ω")
    assert "10 Ω" in parallel_prompt and "20 Ω" in parallel_prompt

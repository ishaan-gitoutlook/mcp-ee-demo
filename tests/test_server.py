from ee_mcp_demo.server import (
    calculate_ohms_law_tool,
    calculate_series_resistance_tool,
    mcp,
    analyze_circuit,
    explain_ohms_law,
)


def test_server_name():
    assert mcp.name == "ee-circuit-tutor"


def test_tool_wrappers_return_circuit_results():
    assert calculate_ohms_law_tool(voltage=9, resistance=3)["current"] == 3
    assert calculate_series_resistance_tool(resistances=[100, 220])["total_resistance"] == 320


def test_resource_and_prompt_content():
    assert "V = I A- R" in explain_ohms_law()
    prompt = analyze_circuit(voltage="12 V", resistance="6 Ic")
    assert "12 V" in prompt and "6 Ic" in prompt

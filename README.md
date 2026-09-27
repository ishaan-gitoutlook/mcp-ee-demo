# EE Circuit Tutor MCP Server

An educational Model Context Protocol (MCP) server demonstrating how to expose basic electrical engineering calculations.

## Concepts
- **Tools**: Actions that the client can execute, like calculating Ohm's Law.
- **Resources**: Reference sheets, like the Ohm's Law cheat sheet.
- **Prompts**: Lab instructions to guide analysis.

## Setup
```bash
uv sync
uv run pytest -q
```

## Inspector
To test manually with the MCP Inspector:
```bash
uv run mcp dev src/ee_mcp_demo/server.py
```

## Components

| Component | Type | Description |
|-----------|------|-------------|
| `calculate_ohms_law` | Tool | Calculates missing value in V = I * R |
| `calculate_series_resistance` | Tool | Adds resistors in series |
| `ee://laws/ohms-law` | Resource | Ohm's law reference sheet |
| `analyze_circuit` | Prompt | Checklist for circuit analysis |

## Example
If you know:
- V = 12 V
- R = 6 Ic

You can solve for I: `I = V / R = 12 / 6 = 2 A`.

> **Safety Note:** This server performs purely educational arithmetic. It is not a substitute for measured values, component ratings, or supervised physical lab work.

## Exercises
- Add parallel resistance calculations.
- Add Power calculation `P = V * I`.
- Create a new resource explaining Kirchhoff's laws and a corresponding test.

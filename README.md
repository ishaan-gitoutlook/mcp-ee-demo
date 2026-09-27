# ⚡ MCP Circuit Sandbox (Enterprise Edition)

Welcome to the **MCP Circuit Sandbox**! This is a robust, enterprise-grade project that demonstrates both **Basic Electrical Engineering (EE)** and the **Model Context Protocol (MCP)**.

## What is MCP?
MCP (Model Context Protocol) is a standard way for AI models to connect to external tools, data, and environments. Instead of an AI just "knowing" things from its training, an MCP server provides the AI with:
- **Tools**: Real-world actions it can perform (like using a calculator).
- **Resources**: Documents it can read (like a cheat sheet).
- **Prompts**: Pre-written templates for asking questions.

## The EE Lab Analogy
To make MCP easier to understand, imagine this server as an **Electrical Engineering Lab**:

| MCP Concept | Lab Equivalent | Examples in this Project |
|-------------|----------------|--------------------------|
| **Tools** | **Calculators / Multimeters** | `calculate_ohms_law`, `calculate_series_resistance`, `calculate_parallel_resistance`, `calculate_electrical_power`, `calculate_coulombs_law`, `calculate_charge` |
| **Resources**| **Cheat Sheets** | `ee://laws/ohms-law`, `ee://laws/kirchhoffs-laws`, `ee://laws/coulombs-law`, `ee://laws/capacitance` |
| **Prompts** | **Lab Manuals / Worksheets** | `analyze_circuit`, `analyze_parallel_circuit` |

## Quick Start Example
If you know:
- **Voltage (V)** = 12 V
- **Resistance (R)** = 6 Ω

You can use the `calculate_ohms_law` tool to solve for **Current (I)**:
`I = V / R = 12 / 6 = 2 A`.

> **Safety Note:** This server performs purely educational arithmetic. It is not a substitute for measured values, component ratings, or supervised physical lab work.

## Getting Started
Please see the [TUTORIAL.ipynb](./TUTORIAL.ipynb) for a step-by-step interactive guide on how to install, test, and use this MCP server.

## How to Run the Server
This project is built using `uv` for package management and `FastMCP`.

To run the MCP Inspector (a web-based UI for testing your MCP tools, resources, and prompts):
```bash
uv run mcp dev src/ee_mcp_demo/server.py
```

To run the MCP server using standard input/output (which is how AI clients will typically connect to it):
```bash
uv run python -m ee_mcp_demo.server
```

## How to Run the Web UI
We also provide an interactive web application built with **Streamlit** that uses the same core calculations. 

To install the optional UI dependencies:
```bash
uv sync --all-extras
```

To launch the web interface:
```bash
make ui
# or
uv run streamlit run src/ee_mcp_demo/ui/app.py
```

---

## Enterprise Architecture
This project is structured following Enterprise Python standards for maintainability, strict typing, and separation of concerns.

### Project Structure
```text
mcp-ee-demo/
├── .github/workflows/ci.yml       # Automated CI/CD pipelines
├── Makefile                       # Developer commands (make check, make test)
├── pyproject.toml                 # Package definition and tool config (ruff, mypy)
├── tests/                         # Unit tests covering all logic and MCP handlers
└── src/ee_mcp_demo/
    ├── app.py                     # FastMCP singleton definition
    ├── server.py                  # Main execution entrypoint
    ├── core/                      # Pure Business Logic
    │   ├── calculations.py        # Electrical engineering formulas
    │   ├── exceptions.py          # Custom domain exceptions
    │   └── logger.py              # Centralized logging configuration
    └── mcp_handlers/              # API / Presentation Layer
        ├── prompts.py             # Registered MCP Prompts
        ├── resources.py           # Registered MCP Resources
        └── tools.py               # Registered MCP Tools
```

### Developer Commands
We use `uv` for lightning-fast package management, `ruff` for linting/formatting, `mypy` for strict static type checking, and `pytest` for unit testing.

If you have `make` installed, you can run all automated checks via:
```bash
make check
```

Or run them individually via `uv`:
```bash
uv run pytest -q                 # Run tests
uv run ruff check src tests      # Run linter
uv run mypy src tests            # Run type checker
```

# Python MCP Electrical Engineering Demo Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a runnable Python MCP server that teaches a first-year electrical engineering student how MCP tools, resources, prompts, schemas, and stdio transport support basic circuit calculations.

**Architecture:** Create an isolated `mcp-ee-demo/` project under `C:/Users/Ishaan`; do not modify the unrelated root Node package. Keep calculations as pure functions in `src/ee_mcp_demo/circuits.py`, expose them through FastMCP in `src/ee_mcp_demo/server.py`, and verify the real protocol through the official MCP Python client and MCP Inspector. Use `uv`, pytest, pytest-asyncio, and the official `mcp[cli]` package.

**Tech Stack:** Python 3.11+, official MCP Python SDK/FastMCP, `uv`, pytest, pytest-asyncio, MCP Inspector.

---

## Current context / assumptions

- Workspace: `C:/Users/Ishaan`; project: `C:/Users/Ishaan/mcp-ee-demo`.
- The root `package.json` is unrelated and must not be changed.
- Git Bash on Windows 11 can run `python`, `uv`, and `git`.
- The learner knows basic voltage, current, resistance, and algebra.
- Keep this simulation-only: no hardware, GPIO, database, HTTP deployment, credentials, or LLM API keys.
- Use `from mcp.server.fastmcp import FastMCP`, `@mcp.tool`, `@mcp.resource`, `@mcp.prompt`, and `mcp.run()`. If the resolved SDK exposes a documented spelling difference, inspect the installed package and make the smallest compatible change.
- Never write diagnostics to stdout; stdout is the stdio JSON-RPC channel.

## Step-by-step tasks

### Task 1: Scaffold the Python project

**Objective:** Create a reproducible Python environment and test command.

**Files:**
- Create: `mcp-ee-demo/pyproject.toml`
- Create: `mcp-ee-demo/.python-version`
- Create: `mcp-ee-demo/src/ee_mcp_demo/__init__.py`
- Create: `mcp-ee-demo/tests/__init__.py`

**Step 1: Create `mcp-ee-demo/pyproject.toml`**

```toml
[project]
name = "ee-mcp-demo"
version = "0.1.0"
description = "A beginner-friendly MCP server for electrical engineering calculations"
readme = "README.md"
requires-python = ">=3.11"
dependencies = ["mcp[cli]>=1.0.0,<2.0.0"]

[dependency-groups]
dev = [
  "pytest>=8.0.0",
  "pytest-asyncio>=0.24.0"
]

[project.scripts]
ee-mcp-server = "ee_mcp_demo.server:main"

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
addopts = "-q"
asyncio_mode = "auto"
```

Create `.python-version` containing `3.11`, and create both package files with:

```python
"""Beginner electrical-engineering MCP demo."""
```

Run:

```bash
cd /c/Users/Ishaan
mkdir -p mcp-ee-demo/src/ee_mcp_demo mcp-ee-demo/tests
cd mcp-ee-demo
uv sync
uv run python -c "from mcp.server.fastmcp import FastMCP; print('FastMCP import OK')"
uv run pytest
```

Expected: `uv.lock` and `.venv/` are created; the import prints `FastMCP import OK`; pytest reports no tests without an import or environment error.

Commit:

```bash
git add mcp-ee-demo/pyproject.toml mcp-ee-demo/uv.lock mcp-ee-demo/.python-version mcp-ee-demo/src mcp-ee-demo/tests
git commit -m "chore: scaffold Python MCP EE demo"
```

---

### Task 2: Implement Ohm's law with TDD

**Objective:** Implement and test the first pure electrical calculation before adding MCP protocol code.

**Files:**
- Create: `mcp-ee-demo/tests/test_circuits.py`
- Create: `mcp-ee-demo/src/ee_mcp_demo/circuits.py`

**Step 1: Write the failing test in `mcp-ee-demo/tests/test_circuits.py`**

```python
import pytest
from ee_mcp_demo.circuits import calculate_ohms_law


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
```

Run `uv run pytest tests/test_circuits.py`. Expected: FAIL during collection because `ee_mcp_demo.circuits` does not exist.

**Step 2: Add `mcp-ee-demo/src/ee_mcp_demo/circuits.py`**

```python
from __future__ import annotations


def calculate_ohms_law(*, voltage=None, current=None, resistance=None):
    values = (voltage, current, resistance)
    if sum(value is not None for value in values) != 2:
        raise ValueError("Provide exactly two of voltage, current, and resistance")
    if voltage is not None and voltage < 0:
        raise ValueError("Voltage cannot be negative in this beginner demo")
    if current is not None and current < 0:
        raise ValueError("Current cannot be negative in this beginner demo")
    if resistance is not None and resistance <= 0:
        raise ValueError("Resistance must be greater than zero")
    if voltage is None:
        assert current is not None and resistance is not None
        return {"voltage": current * resistance, "current": current, "resistance": resistance, "solved_for": "voltage", "unit": "V"}
    if current is None:
        assert resistance is not None
        return {"voltage": voltage, "current": voltage / resistance, "resistance": resistance, "solved_for": "current", "unit": "A"}
    if current == 0:
        raise ValueError("Current must be greater than zero when solving resistance")
    return {"voltage": voltage, "current": current, "resistance": voltage / current, "solved_for": "resistance", "unit": "Ω"}
```

Run `uv run pytest tests/test_circuits.py`. Expected: `3 passed`.

Commit:

```bash
git add mcp-ee-demo/src/ee_mcp_demo/circuits.py mcp-ee-demo/tests/test_circuits.py
git commit -m "feat: add tested Ohms law calculation"
```

---

### Task 3: Add series resistance with TDD

**Objective:** Add a second small EE calculation and its validation tests.

**Files:**
- Modify: `mcp-ee-demo/src/ee_mcp_demo/circuits.py`
- Modify: `mcp-ee-demo/tests/test_circuits.py`

**Step 1: Add failing tests**

Append to `tests/test_circuits.py`:

```python
from ee_mcp_demo.circuits import calculate_series_resistance


def test_adds_series_resistors():
    assert calculate_series_resistance([100, 220, 330]) == {
        "resistances": [100, 220, 330],
        "total_resistance": 650,
        "unit": "Ω",
    }


def test_rejects_empty_or_non_positive_resistors():
    with pytest.raises(ValueError, match="at least one"):
        calculate_series_resistance([])
    with pytest.raises(ValueError, match="greater than zero"):
        calculate_series_resistance([100, 0])
```

Run `uv run pytest tests/test_circuits.py`. Expected: original 3 pass and the 2 new tests fail because the function is undefined.

**Step 2: Append to `src/ee_mcp_demo/circuits.py`**

```python
def calculate_series_resistance(resistances: list[float]) -> dict[str, object]:
    if not resistances:
        raise ValueError("Provide at least one resistor")
    if any(resistance <= 0 for resistance in resistances):
        raise ValueError("Every resistance must be greater than zero")
    return {
        "resistances": resistances,
        "total_resistance": sum(resistances),
        "unit": "Ω",
    }
```

Run `uv run pytest tests/test_circuits.py`. Expected: `5 passed`.

Commit:

```bash
git add mcp-ee-demo/src/ee_mcp_demo/circuits.py mcp-ee-demo/tests/test_circuits.py
git commit -m "feat: add tested series resistance calculation"
```

---

### Task 4: Expose calculations as FastMCP tools

**Objective:** Register two typed MCP tools while keeping business logic in `circuits.py`.

**Files:**
- Create: `mcp-ee-demo/src/ee_mcp_demo/server.py`
- Create: `mcp-ee-demo/tests/test_server.py`

**Step 1: Write the failing tests in `tests/test_server.py`**

```python
from ee_mcp_demo.server import calculate_ohms_law_tool, calculate_series_resistance_tool, mcp


def test_server_name():
    assert mcp.name == "ee-circuit-tutor"


def test_tool_wrappers_return_circuit_results():
    assert calculate_ohms_law_tool(voltage=9, resistance=3)["current"] == 3
    assert calculate_series_resistance_tool(resistances=[100, 220])["total_resistance"] == 320
```

Run `uv run pytest tests/test_server.py`. Expected: FAIL during collection because `server.py` does not exist.

**Step 2: Create `src/ee_mcp_demo/server.py`**

```python
from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from ee_mcp_demo.circuits import calculate_ohms_law, calculate_series_resistance

mcp = FastMCP("ee-circuit-tutor")


@mcp.tool(name="calculate_ohms_law")
def calculate_ohms_law_tool(voltage: float | None = None, current: float | None = None, resistance: float | None = None):
    """Calculate the missing value in V = I × R. Provide exactly two values."""
    return calculate_ohms_law(voltage=voltage, current=current, resistance=resistance)


@mcp.tool(name="calculate_series_resistance")
def calculate_series_resistance_tool(resistances: list[float]):
    """Add resistors connected in series: R_total = R1 + R2 + ..."""
    return calculate_series_resistance(resistances)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
```

Run:

```bash
uv run pytest tests/test_server.py
uv run python -c "from ee_mcp_demo.server import mcp; print(mcp.name)"
```

Expected: `2 passed`, then `ee-circuit-tutor`. If the installed SDK rejects the decorator keyword, use its documented equivalent while preserving both names and signatures. Do not add stdout logging.

Commit:

```bash
git add mcp-ee-demo/src/ee_mcp_demo/server.py mcp-ee-demo/tests/test_server.py
git commit -m "feat: expose circuit calculations as MCP tools"
```

---

### Task 5: Add a resource and prompt with TDD

**Objective:** Demonstrate read-only educational context and reusable analysis instructions.

**Files:**
- Modify: `mcp-ee-demo/src/ee_mcp_demo/server.py`
- Modify: `mcp-ee-demo/tests/test_server.py`

**Step 1: Add failing tests**

Append:

```python
from ee_mcp_demo.server import analyze_circuit, explain_ohms_law


def test_resource_and_prompt_content():
    assert "V = I × R" in explain_ohms_law()
    prompt = analyze_circuit(voltage="12 V", resistance="6 Ω")
    assert "12 V" in prompt and "6 Ω" in prompt
```

Run `uv run pytest tests/test_server.py`. Expected: the two tool tests pass and this test fails because the names are undefined.

**Step 2: Insert before `main()` in `server.py`**

```python

@mcp.resource("ee://laws/ohms-law")
def explain_ohms_law() -> str:
    """Reference sheet for Ohm's law."""
    return "\n".join([
        "Ohm's law: V = I × R",
        "V is voltage in volts (V).",
        "I is current in amperes (A).",
        "R is resistance in ohms (Ω).",
        "Choose any two values to calculate the third.",
    ])


@mcp.prompt()
def analyze_circuit(voltage: str, resistance: str) -> str:
    """Create a beginner-friendly checklist for a simple resistive circuit."""
    return (
        f"Analyze this circuit step by step. Known voltage: {voltage}. "
        f"Known resistance: {resistance}. State V = I × R, calculate current, "
        "include units, and mention one assumption."
    )
```

Run `uv run pytest -q`. Expected: `9 passed`.

Commit:

```bash
git add mcp-ee-demo/src/ee_mcp_demo/server.py mcp-ee-demo/tests/test_server.py
git commit -m "feat: add Ohms law resource and analysis prompt"
```

---

### Task 6: Verify the real stdio protocol

**Objective:** Prove that an MCP client can initialize the Python server, discover capabilities, read the resource, and call a tool.

**Files:**
- Create: `mcp-ee-demo/tests/test_stdio_smoke.py`

**Step 1: Write `tests/test_stdio_smoke.py`**

```python
import sys

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_server_works_over_stdio():
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "ee_mcp_demo.server"],
    )
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert {tool.name for tool in tools.tools} >= {
                "calculate_ohms_law",
                "calculate_series_resistance",
            }
            resource = await session.read_resource("ee://laws/ohms-law")
            assert "V = I × R" in str(resource.contents[0])
            result = await session.call_tool(
                "calculate_ohms_law",
                {"voltage": 9, "resistance": 3},
            )
            assert '"current": 3' in str(result.content)
```

**Step 2: Run the test**

Run `uv run pytest tests/test_stdio_smoke.py -q`. Expected: FAIL with an actionable SDK/API or server wiring error if anything remains incomplete; it must not hang.

**Step 3: Make the smallest compatibility correction**

If the installed SDK uses a different `read_resource`, `call_tool`, or stdio import signature, inspect installed Python type hints and adjust only this test or the corresponding documented server API. Keep `sys.executable -m ee_mcp_demo.server` so the test uses the same environment.

**Step 4: Run the complete suite and Inspector**

```bash
uv run pytest -q
uv run mcp dev src/ee_mcp_demo/server.py
```

Expected: all tests pass; Inspector shows `ee-circuit-tutor`, exactly two tools, resource `ee://laws/ohms-law`, and prompt `analyze_circuit`. Calling Ohm's law with 12 V and 6 Ω returns current 2 A.

Commit:

```bash
git add mcp-ee-demo/tests/test_stdio_smoke.py mcp-ee-demo/uv.lock
git commit -m "test: verify Python MCP server over stdio"
```

---

### Task 7: Document the teaching flow and finish quality checks

**Objective:** Make a fresh checkout self-explanatory for the student.

**Files:**
- Create: `mcp-ee-demo/README.md`
- Create: `mcp-ee-demo/.gitignore`

**Step 1: Create `.gitignore`**

```gitignore
.venv/
__pycache__/
.pytest_cache/
*.py[cod]
.env
```

**Step 2: Create `README.md` containing**

- A plain-language explanation of MCP.
- The EE analogy: tools are actions, resources are reference sheets, prompts are lab instructions.
- Setup: `uv sync` followed by `uv run pytest -q`.
- Inspector command: `uv run mcp dev src/ee_mcp_demo/server.py`.
- A table mapping `Tool`, `Resource`, `Prompt`, type-hint schema, pure calculation, and stdio transport to exact files.
- Worked example: `V = 12 V`, `R = 6 Ω`, so `I = V/R = 2 A`.
- Safety note that this is educational arithmetic, not a substitute for measured values, component ratings, or supervised lab work.
- Extension exercises: parallel resistance, power `P = V × I`, and a new resource with a test.

**Step 3: Final verification**

```bash
cd /c/Users/Ishaan/mcp-ee-demo
uv sync
uv run pytest -q
git diff --check
git status --short
git log --oneline -7
```

Expected: all tests pass; `git diff --check` prints nothing; status has no unintended files; the log shows focused commits. Run Inspector once more and manually confirm the two tools, one resource, and one prompt.

**Step 4: Commit documentation**

```bash
git add mcp-ee-demo/README.md mcp-ee-demo/.gitignore
git commit -m "docs: explain Python MCP EE demo for beginners"
```

## Tests / validation summary

- Each code task follows RED → verify failure → minimal implementation → verify pass → commit.
- Unit tests cover Ohm's law, invalid inputs, series resistance, and boundary values.
- Server tests cover tool wrappers, resource content, and prompt content.
- The stdio test uses a real MCP client, not only direct Python calls.
- `uv run pytest -q` and MCP Inspector are required final gates.

## Risks, tradeoffs, and open questions

- **SDK drift:** Official MCP Python and standalone FastMCP examples differ across releases. Use `mcp[cli]`, preserve `uv.lock`, and inspect installed signatures rather than mixing APIs.
- **Windows stdio:** `sys.executable -m ee_mcp_demo.server` avoids shell quoting and interpreter mismatch.
- **Stdout contamination:** Any `print()` from the server can corrupt JSON-RPC; use stderr for diagnostics.
- **Floating point:** Leave raw Python numeric results visible for teaching; add formatting only with an explicit requirement and test.
- **Schema versus domain validation:** FastMCP derives schemas from type hints; pure functions retain validation for direct and protocol calls.
- **Hardware safety:** This demo performs no live electrical control and must not be presented as a substitute for supervised lab work.
- **Host configuration:** Do not add a host-specific JSON configuration until the target MCP host is known; Inspector is the portable baseline.

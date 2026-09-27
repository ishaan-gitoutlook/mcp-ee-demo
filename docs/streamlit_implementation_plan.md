## Goal Description
Add a web-based user interface using **Streamlit** to expose the electrical engineering calculations visually. This will allow users to interact with the project directly via a web browser, in addition to the existing MCP (Model Context Protocol) interface.

## User Review Required
- **Optional Dependencies:** Instead of making `streamlit` a hard requirement for the whole project (which would bloat the core MCP package), we will add it as an "optional dependency" (an `extra` package).
- **Directory Structure:** I will place the Streamlit app inside `src/ee_mcp_demo/ui/app.py`.

## Proposed Changes

### `pyproject.toml`
#### [MODIFY] pyproject.toml
We will add `streamlit` as an optional dependency:
```toml
[project.optional-dependencies]
ui = ["streamlit>=1.30.0"]
```

### `src/ee_mcp_demo/ui/`
#### [NEW] src/ee_mcp_demo/ui/__init__.py
#### [NEW] src/ee_mcp_demo/ui/app.py
This will be the main Streamlit application script. It will feature:
1. A **Sidebar** to switch between different electrical calculators.
2. Direct imports from `ee_mcp_demo.core.calculations` to ensure the core logic remains decoupled.
3. Graceful error handling using `st.error()` to catch our custom `InvalidParameterError` and `MissingParameterError`.

### `README.md` & `Makefile`
#### [MODIFY] README.md
Add instructions on how to install with the UI extras and launch the app.
#### [MODIFY] Makefile
Add a new command `make ui` to run the app quickly.

## Verification Plan
### Automated Tests
Run the standard suite (`uv run pytest`, `ruff`, `mypy`) to ensure core stability is maintained. Note: `mypy` will be configured to ignore missing imports for `streamlit` if necessary.

### Manual Verification
1. Run `uv run streamlit run src/ee_mcp_demo/ui/app.py`
2. Open the browser link (`http://localhost:8501`).
3. Manually test solving Ohm's Law and adding resistors in parallel to ensure the logic and error handling render correctly on the frontend.

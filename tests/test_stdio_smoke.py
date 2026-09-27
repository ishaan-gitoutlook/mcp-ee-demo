import os
import sys

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_server_works_over_stdio() -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "ee_mcp_demo.server"],
        env=env,
    )
    async with (
        stdio_client(parameters) as (read_stream, write_stream),
        ClientSession(read_stream, write_stream) as session,
    ):
        await session.initialize()
        tools = await session.list_tools()
        assert {tool.name for tool in tools.tools} >= {
            "calculate_ohms_law",
            "calculate_series_resistance",
        }
        resource = await session.read_resource("ee://laws/ohms-law")  # type: ignore
        assert "V = I × R" in str(resource.contents[0])
        result = await session.call_tool(
            "calculate_ohms_law",
            {"voltage": 9, "resistance": 3},
        )
        assert '"current": 3' in str(result.content)

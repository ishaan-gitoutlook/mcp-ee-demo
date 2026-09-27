import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_mcp_client():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "ee_mcp_demo.server"],
    )

    async with stdio_client(server_params, errlog=sys.__stderr__) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("Connected!")

asyncio.run(run_mcp_client())

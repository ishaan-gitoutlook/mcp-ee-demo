from mcp.server.fastmcp import FastMCP

from ee_mcp_demo.core.logger import get_logger

logger = get_logger(__name__)

# Initialize the MCP server. This is the main application that clients will connect to.
mcp = FastMCP("mcp-circuit-sandbox")

logger.info("MCP Application initialized")

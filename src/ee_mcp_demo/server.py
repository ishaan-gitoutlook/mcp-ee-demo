import ee_mcp_demo.mcp_handlers.prompts
import ee_mcp_demo.mcp_handlers.resources

# Important: We must import these modules so that the decorators are executed
# and the tools, resources, and prompts are registered with the mcp instance.
import ee_mcp_demo.mcp_handlers.tools  # noqa: F401
from ee_mcp_demo.app import logger, mcp


def main() -> None:
    """Entry point for the MCP server."""
    logger.info("Starting MCP server...")
    mcp.run()


if __name__ == "__main__":
    main()
